"""Hand-written syllabus entries.

Editorial bar for anything in this list: it must let a normal person do something
that was impossible or wildly impractical before it existed. "Faster" is not enough.

`what_you_can_build` is one concrete item per line — the frontend splits on newlines.
"""

SUBJECTS = [
    {
        "slug": "rag",
        "title": "RAG — Retrieval-Augmented Generation",
        "category": "build",
        "became_usable_on": "2023-03-01",
        "date_note": (
            "No launch day — the technique is from a 2020 paper. Dated to the cheap chat API "
            "that made it practical; LangChain's first release (Oct 2022) is an equally fair "
            "anchor."
        ),
        "resource_url": "https://www.anthropic.com/news/contextual-retrieval",
        "source_url": "https://openai.com/index/introducing-chatgpt-and-whisper-apis/",
        "one_liner": (
            "Give a language model your own documents at question time, so it answers "
            "from your material instead of from what it memorised during training."
        ),
        "what_you_can_build": (
            "A chatbot that answers from your company handbook, contracts, or product docs\n"
            "Customer support that cites the exact paragraph it got the answer from\n"
            "A search box over years of meeting notes that answers questions instead of "
            "returning ten blue links\n"
            "A study assistant that only knows your lecture slides"
        ),
        "before_this": (
            "You wrote FAQ pages by hand and hoped the wording matched what people typed. "
            "Anything smarter meant a keyword search engine plus a team to tune synonyms, "
            "and it still could not answer a question that spanned two documents."
        ),
        "why_new": (
            "Answering a question that requires reading and combining several documents "
            "used to require a human reader. Keyword search could point you at files; it "
            "could not read them for you. Now a machine reads the relevant pages and "
            "writes the answer, and you can point it at private material it has never seen."
        ),
    },
    {
        "slug": "ai-assisted-coding",
        "title": "AI-assisted coding",
        "category": "build",
        "became_usable_on": "2022-06-21",
        "resource_url": "https://code.claude.com/docs",
        "source_url": (
            "https://github.blog/news-insights/product-news/"
            "github-copilot-is-generally-available-to-all-developers/"
        ),
        "one_liner": (
            "An editor that writes the next few lines for you and answers questions about "
            "the code in front of you."
        ),
        "what_you_can_build": (
            "Working scripts in a language you have never learned\n"
            "Tests for code you already wrote, in one keystroke\n"
            "An explanation of a file someone else wrote five years ago\n"
            "Boilerplate — forms, API clients, config — without typing it"
        ),
        "before_this": (
            "You searched Stack Overflow, adapted a stranger's snippet, and read library "
            "docs until the shape of the API was in your head. Autocomplete could finish a "
            "variable name; it could not finish a thought."
        ),
        "why_new": (
            "Programming used to be gated on recall — you had to hold syntax and API "
            "details in memory. Now you can describe intent in English and get working "
            "code, which means people who are not programmers ship small programs, and "
            "programmers work in languages they do not know."
        ),
    },
    {
        "slug": "coding-agents",
        "title": "Coding agents",
        "category": "agents",
        "became_usable_on": "2025-02-24",
        "resource_url": "https://code.claude.com/docs",
        "source_url": "https://www.anthropic.com/news/claude-3-7-sonnet",
        "one_liner": (
            "A model that works in your actual repository — reads files, edits them, runs "
            "the tests, and fixes what it broke — instead of handing you a snippet."
        ),
        "what_you_can_build": (
            "A whole feature from a paragraph of description, delivered as a pull request\n"
            "A dependency upgrade across two hundred files\n"
            "A bug fix from nothing but a stack trace and a failing test\n"
            "A migration from one framework to another, done overnight"
        ),
        "before_this": (
            "You copied code out of a chat window, pasted it in, ran it, copied the error "
            "back, and repeated. Every loop needed a human in the middle to move text "
            "between two windows."
        ),
        "why_new": (
            "The loop closed. A model that can run the code sees whether it worked and "
            "tries again — so tasks that take hours of iteration can be handed over whole "
            "rather than one snippet at a time. Multi-file changes stopped being a human-"
            "only job."
        ),
    },
    {
        "slug": "mcp",
        "title": "MCP — Model Context Protocol",
        "category": "infra",
        "became_usable_on": "2024-11-25",
        "resource_url": "https://modelcontextprotocol.io",
        "source_url": "https://www.anthropic.com/news/model-context-protocol",
        "one_liner": (
            "A standard plug shape for connecting AI assistants to tools and data — one "
            "connector per service, usable by any assistant that speaks it."
        ),
        "what_you_can_build": (
            "Give your assistant read access to your Postgres, Slack, or Google Drive in "
            "minutes\n"
            "Wrap your own internal API once and have every AI tool in the company use it\n"
            "Swap the model behind your assistant without rewriting a single integration\n"
            "A local server that exposes your filesystem to a model, with the permissions "
            "you choose"
        ),
        "before_this": (
            "Every AI product built its own bespoke plugin format. Connecting an assistant "
            "to your database meant writing glue code specific to that one vendor, and "
            "throwing it away when you switched."
        ),
        "why_new": (
            "Integrations became portable. Before, the work of connecting a model to a "
            "system was locked to whichever vendor you connected it to — so nobody built "
            "connectors for niche systems. A shared protocol made a long tail of "
            "integrations worth writing once."
        ),
    },
    {
        "slug": "tool-use",
        "title": "Tool use — models that call your functions",
        "category": "agents",
        "became_usable_on": "2023-06-13",
        "resource_url": "https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview",
        "source_url": "https://openai.com/index/function-calling-and-other-api-updates/",
        "one_liner": (
            "You describe the functions a model is allowed to call; it decides when to call "
            "them and what to pass in, then uses the result."
        ),
        "what_you_can_build": (
            "An assistant that actually books the meeting instead of describing how to\n"
            "A support bot that looks up a real order status before answering\n"
            "A model that does arithmetic by calling a calculator instead of guessing\n"
            "Anything where the answer depends on live data the model cannot know"
        ),
        "before_this": (
            "Models could only produce text. To make one act, you parsed its output with "
            "regular expressions and hoped the format held. It broke constantly."
        ),
        "why_new": (
            "This is the hinge that turned a text generator into something that can do "
            "things. Every agent, every assistant that touches a real system, sits on top "
            "of it — before it, an AI could tell you what to do but never do it."
        ),
    },
    {
        "slug": "structured-outputs",
        "title": "Structured outputs",
        "category": "build",
        "became_usable_on": "2024-08-06",
        "resource_url": "https://platform.claude.com/docs/en/build-with-claude/structured-outputs",
        "source_url": "https://openai.com/index/introducing-structured-outputs-in-the-api/",
        "one_liner": (
            "Hand the model a schema and get back JSON that always matches it — no parsing, "
            "no retries, no cleanup."
        ),
        "what_you_can_build": (
            "Turn a pile of messy resumes into a clean spreadsheet\n"
            "Extract line items, dates, and totals from any invoice layout\n"
            "Classify thousands of support tickets into your own categories\n"
            "Put an AI step in the middle of a normal program without the program breaking"
        ),
        "before_this": (
            "You begged in the prompt for valid JSON, then wrote a parser, a retry loop, "
            "and a repair function for when the model added a friendly sentence before the "
            "opening brace."
        ),
        "why_new": (
            "It made AI safe to put inside ordinary software. Unpredictable output can be "
            "read by a human but not consumed by a program; a guaranteed shape means an AI "
            "step can sit in a pipeline like any other function call."
        ),
    },
    {
        "slug": "embeddings-semantic-search",
        "title": "Embeddings and semantic search",
        "category": "build",
        "became_usable_on": "2022-12-15",
        "resource_url": "https://platform.claude.com/docs/en/build-with-claude/embeddings",
        "source_url": "https://openai.com/index/new-and-improved-embedding-model/",
        "one_liner": (
            "Turn text, images, or audio into coordinates, so things that mean the same "
            "thing land near each other — searchable by meaning rather than by wording."
        ),
        "what_you_can_build": (
            "Search that finds 'cannot log in' when the ticket says 'password rejected'\n"
            "Duplicate detection across support tickets or bug reports\n"
            "Recommendations based on what content is actually about\n"
            "Clustering ten thousand survey responses into themes nobody defined in advance"
        ),
        "before_this": (
            "Search matched words. Finding related items meant maintaining synonym lists "
            "and tag taxonomies by hand, and re-tagging everything whenever the vocabulary "
            "of your users drifted."
        ),
        "why_new": (
            "Meaning became measurable, cheaply and at scale. 'Find things like this one' "
            "used to require a human to define what 'like' meant, category by category — "
            "now it is a distance calculation over any pile of text you have."
        ),
    },
    {
        "slug": "n8n-ai-automation",
        "title": "AI in workflow automation (n8n, Make, Zapier)",
        "category": "automate",
        "became_usable_on": "2023-12-01",
        "date_note": (
            "Three vendors, no shared date. Dated to n8n's LangChain nodes (1.19.4); "
            "Zapier's AI Actions landed 6 Nov 2023."
        ),
        "resource_url": "https://n8n.io",
        "source_url": "https://github.com/n8n-io/n8n/releases/tag/n8n%401.19.4",
        "one_liner": (
            "Drag-and-drop automation tools with a language model as one of the boxes, so "
            "steps that need judgement stop needing a person."
        ),
        "what_you_can_build": (
            "Every inbound email read, categorised, and routed to the right person\n"
            "New form submissions summarised into a daily Slack digest\n"
            "Invoices from twenty different suppliers turned into one consistent "
            "spreadsheet\n"
            "A weekly report that reads the week's data and writes the commentary"
        ),
        "before_this": (
            "Automation could only handle rules you could state in advance: if subject "
            "contains X, do Y. Anything requiring reading and judgement fell out of the "
            "flow and onto somebody's desk."
        ),
        "why_new": (
            "The judgement step got automated, not just the plumbing. Zapier could move "
            "data between apps for a decade; what it could not do was decide whether an "
            "email was a complaint. Now the whole chain runs unattended."
        ),
    },
    {
        "slug": "speech-to-text",
        "title": "Speech-to-text that actually works",
        "category": "interface",
        "became_usable_on": "2022-09-21",
        "resource_url": "https://github.com/openai/whisper",
        "source_url": "https://openai.com/index/whisper/",
        "one_liner": (
            "Accurate transcription of ordinary speech — accents, background noise, "
            "multiple languages — cheap enough to run on everything you record."
        ),
        "what_you_can_build": (
            "Searchable transcripts of every meeting your team has ever had\n"
            "Subtitles for your entire video back-catalogue, in several languages\n"
            "Voice notes that become written tasks\n"
            "Call-centre recordings turned into text you can analyse in bulk"
        ),
        "before_this": (
            "You paid human transcribers by the audio hour, or used dictation software that "
            "needed training on your voice and fell apart on a second speaker or a noisy "
            "room."
        ),
        "why_new": (
            "Transcription went from a per-hour cost to effectively free, which changed "
            "what you transcribe. Nobody transcribed every meeting at £1 a minute — at "
            "near zero, spoken conversation becomes a searchable archive."
        ),
    },
    {
        "slug": "voice-cloning-tts",
        "title": "Natural text-to-speech and voice cloning",
        "category": "media",
        "became_usable_on": "2023-01-23",
        "date_note": (
            "ElevenLabs opened its public beta on this date; it left beta on 22 Aug 2023."
        ),
        "resource_url": "https://elevenlabs.io",
        "source_url": (
            "https://elevenlabs.io/blog/elevenlabs-comes-out-of-beta-and-releases-"
            "eleven-multilingual-v2-a-foundational-ai-speech-model-for-nearly-30-languages"
        ),
        "one_liner": (
            "Speech synthesis that sounds like a person rather than a robot, in any voice "
            "you have a short sample of."
        ),
        "what_you_can_build": (
            "An audiobook of your own writing, in your own voice\n"
            "Course videos dubbed into eight languages with one narrator\n"
            "Voiced characters in a game made by two people\n"
            "Accessible versions of long articles that people will actually listen to"
        ),
        "before_this": (
            "You booked a studio and a voice actor, or you shipped the flat robotic voice "
            "of a screen reader. Changing one sentence meant booking the session again."
        ),
        "why_new": (
            "Editing audio narration used to mean re-recording it. Now a script change is a "
            "text edit, and a one-person project can ship the kind of voiced content that "
            "used to require a budget and a booth."
        ),
    },
    {
        "slug": "realtime-voice-agents",
        "title": "Realtime voice agents",
        "category": "interface",
        "became_usable_on": "2024-10-01",
        "resource_url": "https://platform.claude.com/docs",
        "source_url": "https://openai.com/index/introducing-the-realtime-api/",
        "one_liner": (
            "Speech in, speech out, fast enough to interrupt — a phone conversation with "
            "software that understands what you mean."
        ),
        "what_you_can_build": (
            "A booking line that handles reschedules at 2am\n"
            "A hands-free assistant for people working with their hands\n"
            "Language practice with a patient partner who never gets bored\n"
            "Phone screening that adapts its questions to the answers"
        ),
        "before_this": (
            "Phone menus. Press 1 for sales. Every branch of the conversation had to be "
            "drawn in advance by a human, and anything unanticipated dead-ended in 'let me "
            "transfer you'."
        ),
        "why_new": (
            "Unscripted spoken conversation with a machine became possible. IVR systems "
            "could only walk a tree somebody drew; a voice agent can handle a request "
            "nobody predicted, and hear you cut in halfway through."
        ),
    },
    {
        "slug": "vision-llms",
        "title": "Models that can see",
        "category": "build",
        "became_usable_on": "2023-09-25",
        "resource_url": "https://platform.claude.com/docs/en/build-with-claude/vision",
        "source_url": "https://openai.com/index/chatgpt-can-now-see-hear-and-speak/",
        "one_liner": (
            "Send an image and ask a question about it in plain language — no training, no "
            "labelled dataset, no fixed list of things it can recognise."
        ),
        "what_you_can_build": (
            "A screenshot of a design turned into working front-end code\n"
            "Photos of a job site checked against a safety checklist\n"
            "A chart in a PDF read back as numbers\n"
            "Alt text for ten thousand images"
        ),
        "before_this": (
            "Computer vision meant collecting thousands of labelled examples and training a "
            "model per task. 'Is this shelf tidy?' was a research project, not a question "
            "you could ask."
        ),
        "why_new": (
            "You can now ask an open-ended question about an image without training "
            "anything. Old vision systems only recognised the categories they were built "
            "for; these answer questions their builders never anticipated."
        ),
    },
    {
        "slug": "document-extraction",
        "title": "Document extraction without templates",
        "category": "automate",
        "became_usable_on": "2024-03-04",
        "resource_url": "https://platform.claude.com/docs/en/build-with-claude/pdf-support",
        "source_url": "https://www.anthropic.com/news/claude-3-family",
        "one_liner": (
            "Pull structured data out of PDFs, scans, and photos regardless of layout — no "
            "per-vendor template to configure."
        ),
        "what_you_can_build": (
            "Supplier invoices from any format into your accounting system\n"
            "Key terms and dates lifted out of a stack of contracts\n"
            "Lab results from scanned reports into a spreadsheet\n"
            "Handwritten forms digitised at the point of collection"
        ),
        "before_this": (
            "OCR gave you a wall of text with no structure. Real extraction meant drawing "
            "boxes on a template for each document layout you handled, and redoing it every "
            "time a supplier redesigned their invoice."
        ),
        "why_new": (
            "The template disappeared. Handling a document layout you have never seen "
            "before used to be impossible by definition — the system only knew the layouts "
            "someone configured. Now the first document from a new supplier just works."
        ),
    },
    {
        "slug": "image-generation",
        "title": "Image generation",
        "category": "media",
        "became_usable_on": "2022-08-22",
        "resource_url": "https://stability.ai",
        "source_url": "https://stability.ai/news-updates/stable-diffusion-public-release",
        "one_liner": "Describe a picture in words and get the picture.",
        "what_you_can_build": (
            "Illustrations for a blog nobody would have paid an illustrator for\n"
            "Concept art and mood boards in an afternoon instead of a fortnight\n"
            "Product mockups before the product exists\n"
            "Storyboards for a video you are still deciding whether to make"
        ),
        "before_this": (
            "You commissioned an illustrator, licensed a stock photo that was nearly right, "
            "or made do with no image at all. Anything specific to your idea cost money and "
            "days."
        ),
        "why_new": (
            "Specific, novel images became free and instant. Stock libraries only held "
            "pictures someone had already taken — if your idea was unusual, no amount of "
            "money-free searching would find it. Now the long tail of images gets made on "
            "demand."
        ),
    },
    {
        "slug": "instruction-image-editing",
        "title": "Editing images by asking",
        "category": "media",
        "became_usable_on": "2023-05-23",
        "resource_url": "https://helpx.adobe.com/photoshop/using/generative-fill.html",
        "source_url": "https://helpx.adobe.com/photoshop/using/whats-new/2023-3.html",
        "one_liner": (
            "Change a photo by describing the change — remove the object, swap the "
            "background, extend the frame — without touching a selection tool."
        ),
        "what_you_can_build": (
            "Clean product shots from photos taken on a phone in a cluttered room\n"
            "One hero image resized for every social format without awkward cropping\n"
            "Old family photos repaired and de-scratched\n"
            "A dozen colourway variants of the same product picture"
        ),
        "before_this": (
            "Photoshop, and the years of practice behind knowing which tool to reach for. "
            "Removing a person from a photo convincingly was a skilled job."
        ),
        "why_new": (
            "Edits that used to demand craft skill became a sentence. The barrier to photo "
            "editing was never the software licence — it was that masking, cloning, and "
            "relighting take training. That barrier is gone."
        ),
    },
    {
        "slug": "video-generation",
        "title": "Video generation",
        "category": "media",
        "became_usable_on": "2024-12-09",
        "resource_url": "https://runwayml.com",
        "source_url": "https://openai.com/index/sora-is-here/",
        "one_liner": (
            "Generate short video clips from a description or a still image, including "
            "camera movement and consistent characters."
        ),
        "what_you_can_build": (
            "Ad concepts to test before committing to a shoot\n"
            "B-roll for footage you never filmed\n"
            "Animated explainers without an animator\n"
            "A music video made by the musician"
        ),
        "before_this": (
            "A camera, a crew, a location, and a schedule — or an animator working for "
            "weeks. Even a five-second clip had a fixed minimum cost in people and time."
        ),
        "why_new": (
            "Moving pictures stopped requiring either a camera pointed at something real or "
            "a person drawing every frame. That is a genuinely new third way to make video, "
            "and it collapses the cost of trying an idea before producing it."
        ),
    },
    {
        "slug": "local-llms",
        "title": "Running models on your own machine",
        "category": "infra",
        "became_usable_on": "2023-03-10",
        "resource_url": "https://ollama.com",
        "source_url": "https://github.com/ggml-org/llama.cpp",
        "one_liner": (
            "Capable open-weight models that run on a laptop — no internet, no API bill, "
            "nothing leaving the building."
        ),
        "what_you_can_build": (
            "Assistants over data that legally cannot leave your network\n"
            "Bulk processing of millions of records without a per-token bill\n"
            "Software that works on a plane, a ship, or a factory floor with no signal\n"
            "Products where you control the model and it cannot be deprecated under you"
        ),
        "before_this": (
            "Every AI feature meant an API call to somebody else's datacentre, your data on "
            "their servers, a bill that scaled with usage, and a model that could change or "
            "vanish without notice."
        ),
        "why_new": (
            "Confidential and offline use became possible at all. Regulated industries and "
            "disconnected environments were simply excluded from AI when the only option "
            "was a remote API — now the model runs where the data already is."
        ),
    },
    {
        "slug": "fine-tuning-lora",
        "title": "Fine-tuning and LoRA",
        "category": "infra",
        "became_usable_on": "2023-02-10",
        "resource_url": "https://huggingface.co/docs/peft",
        "source_url": "https://huggingface.co/blog/peft",
        "one_liner": (
            "Nudge an existing model toward your style, format, or niche vocabulary using a "
            "few hundred examples and a modest budget."
        ),
        "what_you_can_build": (
            "A model that writes in your company's voice without a 2,000-word prompt\n"
            "An image model that draws your specific characters or products consistently\n"
            "A small, cheap model that matches a big one on your one narrow task\n"
            "A classifier for jargon no general model has seen"
        ),
        "before_this": (
            "Specialising a model meant training one from scratch: a research team, a "
            "labelled dataset in the millions, and a cluster of GPUs for weeks."
        ),
        "why_new": (
            "Customising a large model came within reach of individuals. The cost fell by "
            "orders of magnitude — from a corporate research budget to an afternoon and a "
            "rented GPU — which put specialised models in the hands of people who could "
            "never have trained one."
        ),
    },
    {
        "slug": "long-context",
        "title": "Long context windows",
        "category": "infra",
        "became_usable_on": "2024-04-09",
        "date_note": (
            "Gemini 1.5 Pro's 1M-token window was announced 15 Feb 2024 but waitlisted; "
            "dated to the day it opened to everyone."
        ),
        "resource_url": "https://platform.claude.com/docs/en/build-with-claude/context-windows",
        "source_url": (
            "https://developers.googleblog.com/en/gemini-15-pro-now-available-in-180-countries"
            "-with-native-audio-understanding-system-instructions-json-mode-and-more/"
        ),
        "one_liner": (
            "Models that hold a whole book, codebase, or year of email in view at once — "
            "hundreds of thousands of words per question."
        ),
        "what_you_can_build": (
            "Questions answered across an entire codebase, not one file\n"
            "A 400-page report analysed in a single pass\n"
            "Legal review that compares a contract against every prior version\n"
            "Assistants that remember a conversation that has run all week"
        ),
        "before_this": (
            "You chopped documents into fragments, retrieved the pieces you hoped were "
            "relevant, and accepted that the model never saw the whole thing. Anything "
            "requiring the full picture was out of reach."
        ),
        "why_new": (
            "Reasoning over a whole large document became possible, not just over excerpts. "
            "Questions like 'is this consistent throughout?' cannot be answered from "
            "fragments — they need everything in view at once."
        ),
    },
    {
        "slug": "computer-use",
        "title": "Computer use and browser agents",
        "category": "agents",
        "became_usable_on": "2024-10-22",
        "resource_url": (
            "https://platform.claude.com/docs/en/agents-and-tools/computer-use/overview"
        ),
        "source_url": "https://www.anthropic.com/news/3-5-models-and-computer-use",
        "one_liner": (
            "A model that looks at a screen and moves the mouse and keyboard — driving "
            "software the way a person does, with no API required."
        ),
        "what_you_can_build": (
            "Automation over legacy internal systems that have no API and never will\n"
            "Filling the same form in three portals that refuse to talk to each other\n"
            "End-to-end testing that adapts when the UI moves\n"
            "Research that spans a dozen sites and ends in a filled spreadsheet"
        ),
        "before_this": (
            "Either the software had an API, or the work stayed manual. Screen-scraping "
            "scripts matched exact pixel positions and broke the moment a button moved."
        ),
        "why_new": (
            "Software without an API became automatable. That was the hard wall in "
            "automation for thirty years — a huge amount of office work lives in systems "
            "that expose nothing programmatically."
        ),
    },
    {
        "slug": "evals-llm-judge",
        "title": "Evals and LLM-as-judge",
        "category": "infra",
        "became_usable_on": "2023-06-09",
        "date_note": (
            "Dated to the LLM-as-judge paper. OpenAI open-sourced the Evals framework "
            "earlier, on 14 Mar 2023."
        ),
        "resource_url": "https://platform.claude.com/docs/en/test-and-evaluate/eval-tool",
        "source_url": "https://arxiv.org/abs/2306.05685",
        "one_liner": (
            "Grade the quality of open-ended output automatically, using a model as the "
            "marker against a written rubric."
        ),
        "what_you_can_build": (
            "A test suite for an AI feature, so you know whether a change made it worse\n"
            "Quality scoring across thousands of support replies\n"
            "A/B comparison of two prompts on real traffic instead of vibes\n"
            "Continuous monitoring that catches a model regression the day it ships"
        ),
        "before_this": (
            "Judging whether a piece of writing is good required a human reading it. "
            "Software testing only worked on outputs with one correct answer, so anything "
            "open-ended was tested by spot-checking and hoping."
        ),
        "why_new": (
            "Subjective quality became measurable at scale. You could always ask five "
            "people to rate a hundred answers; you could never ask them to rate a hundred "
            "thousand, every time you changed a line."
        ),
    },
    {
        "slug": "text-to-sql",
        "title": "Text-to-SQL and natural-language BI",
        "category": "build",
        "became_usable_on": "2023-07-06",
        "resource_url": "https://platform.claude.com/docs",
        "source_url": "https://x.com/OpenAI/status/1677015057316872192",
        "one_liner": (
            "Ask a question about your data in English; get the query, the numbers, and the chart."
        ),
        "what_you_can_build": (
            "Self-serve analytics for a team with no analyst\n"
            "A Slack bot that answers 'how did we do last week' from the live database\n"
            "Dashboards that answer the follow-up question, not just the first one\n"
            "Ad-hoc investigation without waiting three days in the data team's queue"
        ),
        "before_this": (
            "You learned SQL, or you filed a ticket with someone who had. Dashboards "
            "answered the questions their builder anticipated and nothing else."
        ),
        "why_new": (
            "The follow-up question became answerable by the person asking it. Pre-built "
            "dashboards were frozen at the moment of design — every genuinely new question "
            "required a specialist and a queue."
        ),
    },
    {
        "slug": "synthetic-data",
        "title": "Synthetic data generation",
        "category": "build",
        "became_usable_on": "2023-03-13",
        "date_note": (
            "No launch event. Dated to Stanford Alpaca, the project that made generating "
            "training data from a model a normal thing to do."
        ),
        "resource_url": "https://platform.claude.com/docs",
        "source_url": "https://github.com/tatsu-lab/stanford_alpaca",
        "one_liner": (
            "Generate realistic-but-fake records, conversations, or examples to test, demo, "
            "or train with."
        ),
        "what_you_can_build": (
            "A demo environment full of plausible data and no real customers in it\n"
            "Edge cases for testing that never appeared in production\n"
            "Training examples for a rare category you only have nine real samples of\n"
            "Load tests with data shaped like the real thing"
        ),
        "before_this": (
            "You copied production data into staging and hoped nobody noticed the privacy "
            "problem, or you generated rows of 'Test User 1' that exercised none of the "
            "messiness real data has."
        ),
        "why_new": (
            "Realistic test data stopped requiring real people's records. Fake data used to "
            "mean obviously fake data — plausible variety could only come from copying "
            "something real, with all the risk that carried."
        ),
    },
]
