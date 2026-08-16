#!/usr/bin/env python3
"""Generate the LaTeX resume (main.tex) from data.yaml.

Reads data.yaml (the source of truth for the resume) and writes a single
main.tex containing the preamble and every rendered section. Run via `make`
or directly:

    python3 generate.py
"""

import os
import sys

import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, "configuration/data.yaml")
OUTPUT_FILE = os.path.join(ROOT, "output/main.tex")

PREAMBLE = r"""% Giorgos Vyronos Curriculum Vitae

%------------------------
\documentclass[letterpaper,10 pt]{article}

\usepackage{amsmath}
\usepackage{latexsym}
\usepackage[margin=1in]{geometry}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{fontawesome5}
\usepackage{multicol}
\setlength{\multicolsep}{-3.0pt}
\setlength{\columnsep}{-1pt}
\usepackage{longtable}
\input{glyphtounicode}
\usepackage{ragged2e}
%----------FONT OPTIONS----------
% sans-serif
% \usepackage[sfdefault]{FiraSans}
% \usepackage[sfdefault]{roboto}
% \usepackage[sfdefault]{noto-sans}
% \usepackage[default]{sourcesanspro}

% serif
% \usepackage{CormorantGaramond}
% \usepackage{charter}
\usepackage[default]{lato}
% \usepackage{times}
\usepackage[T1]{fontenc}

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.6in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1.19in}
\addtolength{\topmargin}{-.7in}
\addtolength{\textheight}{1.4in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}
\setlength{\footskip}{4.08003pt}
% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\Large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1
\usepackage{amssymb}
\setlist[itemize]{leftmargin=*,label={$\bullet$}}
%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\classesList}[4]{
    \item\small{
        {#1 #2 #3 #4 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{1.0\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{#1} & \textbf{#2}\\
        \textit{\small\emph{#3}} & \textit{\small #4}\\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{1.001\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & \textbf{\small #2}\\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemi{$\vcenter{\hbox{\tiny$\bullet$}}$}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
\usepackage{ulem}
\renewcommand{\ULdepth}{1.8pt}
%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\begin{document}

"""

POSTAMBLE = r"""
\end{document}
"""


def render_link(url, label):
    """Render a \\href wrapper if a URL is present, otherwise the plain label."""
    if url:
        return r"\href{%s}{%s}" % (url, label)
    return label


def render_social(s):
    icon = "\\" + s["icon"]
    return r"\href{%s}{\raisebox{-0.05\height}%s\ %s}" % (
        s["url"], icon, s["text"])


def render_intro(d):
    left1 = r"\textbf{\href{%s}{\huge %s}}" % (d["website_url"], d["name"])
    left2 = r"\href{mailto:%s}{\faEnvelope\ %s}" % (d["email"], d["email"])
    left3 = r"\faMapMarker* %s" % d["location"]

    socials = d.get("socials", [])
    row1_right = r" $\mid$ ".join(render_social(s) for s in socials[:2])
    row2_right = r" $\mid$ ".join(render_social(s) for s in socials[2:])
    website_label = d.get("website_label") or d["website_url"]
    row3_right = r"\href{%s}{\raisebox{-0.05\height}\faMousePointer\ %s}" % (
        d["website_url"], website_label)

    return "\n".join([
        "%-----------INTRODUCTION-----------",
        r"\begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}",
        r"  %s & %s\\" % (left1, row1_right),
        r" %s & %s\\" % (left2, row2_right),
        r" %s & %s\\" % (left3, row3_right),
        r"\end{tabular*}",
        r"\vspace{-10pt}",
    ])


def render_subheading(heading, dates, org, location):
    return [
        r"      \resumeSubheading",
        r"      {%s}{%s}" % (heading, dates),
        r"      {%s}{%s}" % (org, location),
        r"      \resumeItemListStart",
    ]


def render_highlights(highlights):
    return [r"        \resumeItem{%s}" % h for h in highlights]


def render_experience(items):
    lines = ["%-----------EXPERIENCE-----------", r"\section{Experience}",
             r"  \resumeSubHeadingListStart"]
    for e in items:
        heading = e["role"]
        if e.get("subtitle"):
            heading += r" $\mid$ \normalfont\textit{%s}" % e["subtitle"]
        lines += render_subheading(
            heading, e["dates"],
            render_link(e.get("company_url"), e["company"]), e["location"])
        lines += render_highlights(e["highlights"])
        lines.append(r"      \resumeItemListEnd")
    lines.append(r"  \resumeSubHeadingListEnd")
    lines.append(r"\vspace{-16pt}")
    return lines


def render_projects(items):
    lines = ["%-----------PROJECTS-----------", r"\section{Projects}",
             r"    \vspace{-5pt}", r"    \resumeSubHeadingListStart"]
    for i, p in enumerate(items):
        name = r"\textbf{%s}" % p["name"]
        if p.get("url"):
            name = r"\textbf{\href{%s}{%s}}" % (p["url"], p["name"])
        heading = name
        if p.get("tech"):
            heading += r" $|$ \normalfont\textit{%s}" % p["tech"]
        lines.append(r"    \resumeProjectHeading")
        lines.append(r"          {%s}{%s}" % (heading, p["dates"]))
        lines.append(r"          \resumeItemListStart")
        lines += render_highlights(p["highlights"])
        lines.append(r"        \resumeItemListEnd")
        if i < len(items) - 1:
            lines.append(r"            \vspace{-13pt}")
    lines.append(r"    \resumeSubHeadingListEnd")
    lines.append(r"\vspace{-15pt}")
    return lines


def render_education(items):
    lines = ["%-----------EDUCATION-----------", r"\section{Education}",
             r"  \resumeSubHeadingListStart"]
    for e in items:
        lines += render_subheading(
            e["degree"], e.get("dates", ""),
            render_link(e.get("school_url"), e["school"]), e["location"])
        lines += render_highlights(e["highlights"])
        lines.append(r"      \resumeItemListEnd")
    lines.append(r"  \resumeSubHeadingListEnd")
    return lines


def render_leadership(items):
    lines = [r"\section{Leadership and Awards}", r"\resumeSubHeadingListStart"]
    for e in items:
        lines += render_subheading(
            e["role"], e["dates"],
            render_link(e.get("organization_url"), e["organization"]),
            e["location"])
        lines += render_highlights(e["highlights"])
        lines.append(r"    \resumeItemListEnd")
    lines.append(r"  \resumeSubHeadingListEnd")
    return lines


def render_skills(categories):
    lines = [r"\section{Technical Skills}", r"\begin{center}"]
    for i, cat in enumerate(categories):
        lines.append(r"\noindent\begin{minipage}{0.3\textwidth}")
        lines.append(r"\centering")
        lines.append(r"\textbf{%s}\\ " % cat["category"])
        lines.append(r"\justifying")
        lines.append(r"\noindent %s" % cat["items"])
        lines.append(r"\vspace{10pt}" if i > 0 else r"\end{minipage}")
        if i > 0:
            lines.append(r"\end{minipage}")
        if i < len(categories) - 1:
            lines.append(r"\hfill\vline\hfill")
    lines.append(r"\end{center}")
    return lines


SECTIONS = [
    ("intro", render_intro),
    ("experience", render_experience),
    ("projects", render_projects),
    ("education", render_education),
    ("leadership_awards", render_leadership),
    ("skills", render_skills),
]


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    sections = []
    for key, renderer in SECTIONS:
        if key not in data:
            continue
        body = renderer(data[key])
        if isinstance(body, str):
            body = [body]
        sections.append("\n".join(body))

    text = PREAMBLE + "\n\n".join(sections) + POSTAMBLE
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print("generated %s" % OUTPUT_FILE)


if __name__ == "__main__":
    sys.exit(main())
