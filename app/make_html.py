
import sys
import os.path
from subprocess import check_output
from markdown import markdown

def mkdirp(d):
    check_output("mkdir -p {}".format(d), shell=True)

def main(args):
    indir = os.path.abspath("./recipes")
    outdir = os.path.abspath("../output")
    my_dir = os.path.split(os.path.abspath(__file__))[0]
    static_dir = os.path.join(my_dir, 'static')
    if args:
        indir = os.path.abspath(args[0])
    if args[1:]:
        outdir = os.path.abspath(args[1])
    template = open(os.path.join(my_dir, 'template.html')).read()
    os.chdir(indir)
    mkdirp(outdir)
    md_files = check_output(r'find . -name \*.md', shell=True).splitlines()
    for mdfile in md_files:
        d, filename = os.path.split(mdfile)
        htmlfn = filename.replace('.md', '.html')
        od = os.path.join(outdir, d)
        mkdirp(od)
        open(os.path.join(od, htmlfn), 'w').write(
            md_to_html(template, open(mdfile).read()))
    html_files = [fn.replace('.md', '.html') for fn in md_files]
    copy_static(static_dir, outdir)
    make_index(outdir, html_files)


def make_index(outdir, html_files):
    index_md_l = []
    if os.path.exists('index.md'):
        index_md_l.append(open('index.md').read())

    by_cat = dict()

    for fn in html_files:
        fn = fn[2:]
        cat = None
        try:
            cat, fn = fn.split(os.sep, 1)
        except:
            pass
        by_cat[cat] = by_cat.get(cat, []) + [fn]

    for cat in sorted(by_cat):
        prefix = ""
        if cat:
            index_md_l.append("\n\n{}\n----".format(humanize(cat)))
            prefix = cat + os.sep
        for fn in sorted(by_cat[cat]):
            if not cat and fn == 'index.html':
                continue
            name = humanize(fn.rsplit('.', 1)[0])
            index_md_l.append("+ [{}]({}{})".format(name, prefix, fn))

    md = "\n".join(index_md_l)
    html = markdown(md)
    open(os.path.join(outdir, 'index.html'), 'w').write(html)


def copy_static(static_dir, outdir):
    check_output("cp -pr {}/* {}".format(static_dir, outdir), shell=True)


def md_to_html(template, md_data):
    title = md_data.split('\n')[0]
    html = markdown(md_data)
    return template.format(title=title, main=html)


def humanize(s):
    return s.replace('_', ' ').capitalize()


if __name__=='__main__':
    main(sys.argv[1:])
