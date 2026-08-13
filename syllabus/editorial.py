"""The editorial bar — single source of truth.

Read by two consumers: `cms/editorial.html` (the human reference at /dashboard/editorial/) and
`crawl_hn.py` (the rubric the model is judged against). CLAUDE.md paraphrases this file for
context; this file is what actually runs.
"""

BAR = (
    "Only add something that unlocks work which was impossible or wildly impractical before."
)

THREE_QUESTIONS = [
    ("What is it?", "One plain sentence. No hype, no marketing voice, no exclamation marks."),
    ("What can I make with it?", "Three or four concrete things, one per line, no bullets."),
    ("What did I have to do before?", "How people coped when this did not exist."),
]

QUALIFIES = [
    "A capability an ordinary person can now use that had no practical route before.",
    "A shift in kind, not degree — the old way was not slower, it was absent.",
    "Durable: still true next quarter, not a launch-week artefact.",
    "General: the capability, not the product that happens to ship it.",
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
    "interface": "New ways to talk to a machine — voice, vision, the screen itself.",
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
it belongs to might be — but if that capability is already in the index below, it is a
duplicate, so set duplicate_of_slug and is_new_subject=false.

When you reject, still fill the content fields with empty strings and pick any category —
only is_new_subject, duplicate_of_slug and reason are read.

Write content in plain English for a smart person who is not an engineer. No hype, no
marketing voice, no exclamation marks."""
