"""The editorial bar: single source of truth.

Read by three consumers: `cms/editorial.html` (the human reference at /dashboard/editorial/),
`crawl_hn.py` (the rubric the model is judged against), and `document()` below, which serves
the same rules to the public /about page over the API. CLAUDE.md paraphrases this file for
context; this file is what actually runs.
"""

BAR = "Add it only if it lets someone do work that was impossible or wildly impractical before."

THREE_QUESTIONS = [
    ("What is it?", "One plain sentence, written the way you would say it out loud."),
    ("What can I make with it?", "Three or four concrete things, one per line, no bullets."),
    ("What did I have to do before?", "How people coped when this did not exist."),
]

QUALIFIES = [
    "A capability an ordinary person can now use that had no practical route before.",
    "No slower version of this existed to be sped up.",
    "Durable enough to still be true next quarter.",
    "General enough to outlive whichever product shipped it first.",
]

DISQUALIFIES = [
    "Faster",
    "Cheaper",
    "A nicer version of an existing tool",
    "Model releases and version bumps",
    "Benchmark results",
    "Funding and acquisition news",
    "Drama and opinion pieces",
]

CATEGORY_NOTES = {
    "build": "Writing and shipping software.",
    "automate": "Getting routine work done without doing it by hand.",
    "agents": "Systems that take multi-step action on your behalf.",
    "media": "Making or editing images, audio, and video.",
    "interface": "New ways to talk to a machine: by voice, or by pointing a camera at it.",
    "infra": "The plumbing: running, serving, and tuning models.",
}

RUBRIC = """You curate a public syllabus of AI capabilities for non-experts.

The syllabus answers three questions per entry: what is it, what can I build with it, and
what was the way before it existed. An entry earns its place ONLY if it unlocks something
that was impossible or wildly impractical before. "Faster", "cheaper", "a better version of
an existing tool", benchmark results, funding news, model releases, drama, and opinion
pieces do NOT qualify.

Reject by default. You are judging a Hacker News story title and URL. Set is_new_subject to
false unless you are confident the story points at a durable new capability an ordinary
person could use. A specific product launch is usually NOT a subject; the general capability
it belongs to might be, but if that capability is already in the index below, it is a
duplicate, so set duplicate_of_slug and is_new_subject=false.

When you reject, still fill the content fields with empty strings and pick any category.
Only is_new_subject, duplicate_of_slug and reason are read.

VOICE. Write the content fields in plain British English for a smart person who is not an
engineer, in the register you would speak in. No hype and no exclamation marks. The rules
below exist because the copy they describe reads as machine-written; follow all of them.

1. No em dashes anywhere. Use a full stop, a comma, a colon, or brackets.
2. Do not stage contrasts. Avoid "X could do A; it could not do B" and "not A, but B".
   State the thing directly instead of setting up a reversal.
3. Do not open a field with an abstraction turning into a verb ("The loop closed",
   "Meaning became measurable", "That barrier is gone"). Open with the concrete fact and
   let the reader draw the conclusion.
4. No three-part lists of the "no X, no Y, no Z" kind, and no rule-of-three noun strings.
5. Do not tell the reader why the entry matters or that the bar is high. Say what happens.
6. Vary the shape. why_new may be one blunt sentence or four long ones. Do not write it to
   the same three-beat pattern every time.
7. Prefer a specific example to a general claim: a named task, a real document, an actual
   job someone stopped doing by hand."""


def document():
    """The bar as one JSON-ready dict, for the public /about page.

    RUBRIC is deliberately left out: it is prompt text addressed to the model, not
    something a reader needs. Everything here is derived, never restated: editing the
    constants above moves the public page, the CMS reference, and the crawler together.
    """
    # Imported lazily so this module stays readable without the Django app registry:
    # it is the rubric source, and crawl_hn imports it before anything else is set up.
    from syllabus.models import Category

    return {
        "bar": BAR,
        "three_questions": [
            {"question": question, "note": note} for question, note in THREE_QUESTIONS
        ],
        "qualifies": QUALIFIES,
        "disqualifies": DISQUALIFIES,
        "categories": [
            {"slug": value, "label": label, "note": CATEGORY_NOTES.get(value, "")}
            for value, label in Category.choices
        ],
    }
