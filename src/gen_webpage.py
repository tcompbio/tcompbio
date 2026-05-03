"""
TCB static site generator.

Generates the TCB website from Jinja2 templates into the docs/ directory.
Optionally fetches editorial board data from OpenReview when credentials are available.
"""
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

YEAR = datetime.today().year


def render_webpage(env, page, base_url, template_kw=None):
    if template_kw is None:
        template_kw = {}
    dest = os.path.join("docs", page)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        template = env.get_template(page)
        out = template.render(
            **template_kw,
            year=YEAR,
            base_url=base_url,
        )
        f.write(out)


def try_get_openreview_data():
    """
    Try to fetch editorial board data from OpenReview.
    Returns empty lists if credentials are not available.
    """
    try:
        import openreview
        from openreview import tools
        import unidecode

        client = openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=os.environ['OR_USER'],
            password=os.environ['OR_PASS'],
        )

        def get_board_members(group_id):
            ids = client.get_group(id=group_id).members
            profiles = tools.get_profiles(client, ids)
            members = []
            for profile in profiles:
                kw = {}
                try:
                    names = sorted(
                        profile.content['names'],
                        key=lambda d: d.get('preferred', False)
                    )[-1]
                    kw['name'] = names.get('fullname') or (
                        names.get('first', '') + ' ' + names.get('last', '')
                    ).strip()
                    kw['url'] = profile.content.get('homepage', '#')
                    if 'history' in profile.content and profile.content['history']:
                        kw['affiliation'] = profile.content['history'][0]['institution']['name']
                    else:
                        kw['affiliation'] = ''
                    expertise = profile.content.get('expertise', [])
                    kw['research'] = ', '.join(
                        ' '.join(e['keywords']) for e in expertise
                    ).capitalize() + ('.' if expertise else '')
                    kw['gscholar'] = profile.content.get('gscholar', None)
                    kw['id'] = profile.id
                    last_parts = kw['name'].rsplit(' ', 1)
                    kw['last_name'] = last_parts[-1]
                    members.append(kw)
                except Exception as exc:
                    print(f'Warning: issue with profile {profile}: {exc}')
            members.sort(key=lambda d: unidecode.unidecode(d.get('last_name', '').capitalize()))
            return members

        return {
            'editors_in_chief': get_board_members('TCB/Editors_In_Chief'),
            'action_editors': get_board_members('TCB/Action_Editors'),
            'managing_editors': get_board_members('TCB/Managing_Editors'),
        }
    except Exception as exc:
        print(f'OpenReview data unavailable ({exc}); using empty lists.')
        return {
            'editors_in_chief': [
                {
                    'name': 'David A Knowles',
                    'url': 'https://daklab.github.io',
                    'affiliation': 'Columbia University & New York Genome Center',
                    'expertise': '',
                }
            ],
            'action_editors': [],
            'managing_editors': [],
        }


def try_get_papers():
    """
    Try to fetch accepted papers from OpenReview.
    Returns an empty list if credentials are not available.
    """
    try:
        import openreview
        from openreview import tools

        client = openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=os.environ['OR_USER'],
            password=os.environ['OR_PASS'],
        )

        accepted = tools.iterget_notes(
            client,
            invitation='TCB/-/Accepted',
            sort='pdate:desc',
        )

        papers = []
        for s in accepted:
            paper = {}
            paper['id'] = s.forum
            paper['title'] = s.content['title']['value']
            paper['openreview'] = f"https://openreview.net/forum?id={s.forum}"
            paper['pdf'] = f"https://openreview.net/pdf?id={s.forum}"
            paper['bibtex'] = s.content.get('_bibtex', {}).get('value', '')
            paper['authors'] = ', '.join(s.content['authors']['value'])
            date = datetime.fromtimestamp(s.pdate / 1000.)
            paper['intdate'] = s.pdate
            paper['year'] = date.year
            paper['month'] = date.strftime("%B")
            paper['certifications'] = []
            try:
                certifications = s.content['certifications']['value']
            except (KeyError, TypeError):
                certifications = {}
            for cert_name, cert_key in [
                ('Outstanding Certification', 'outstanding'),
                ('Featured Certification', 'featured'),
                ('Software Certification', 'software'),
                ('Reproducibility Certification', 'reproducibility'),
                ('Survey Certification', 'survey'),
            ]:
                if cert_name in certifications:
                    paper['certifications'].append(cert_key)
            if 'code' in s.content:
                paper['code'] = s.content['code']['value']
            papers.append(paper)
        return papers
    except Exception as exc:
        print(f'Papers data unavailable ({exc}); using empty list.')
        return []


def gen_bibtex(papers):
    os.makedirs(os.path.join("docs", "papers", "bib"), exist_ok=True)
    for p in papers:
        bib_path = os.path.join("docs", "papers", "bib", f"{p['id']}.bib")
        with open(bib_path, "w") as f:
            f.write(p['bibtex'])


if __name__ == "__main__":
    base_url = ""

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    board = try_get_openreview_data()
    papers = try_get_papers()

    context = {
        **board,
        'papers': papers,
    }

    gen_bibtex(papers)

    pages = [
        "index.html",
        "submissions.html",
        "contact.html",
        "editorial-board.html",
        "reviewer-guide.html",
        "author-guide.html",
        "acceptance-criteria.html",
        "ae-guide.html",
        "editorial-policies.html",
        "code.html",
        "faq.html",
        "news/index.html",
        "papers/index.html",
        "ethics.html",
    ]

    for page in pages:
        render_webpage(env, page, base_url, context)
        print(f"Generated {page}")

    print("Done. Output written to docs/")
