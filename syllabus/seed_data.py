"""Hand-written syllabus entries.

Editorial bar for anything in this list: it must let a normal person do something
that was impossible or wildly impractical before it existed. "Faster" is not enough.

`what_you_can_build` is one concrete item per line; the frontend splits on newlines.
"""

SUBJECTS = [
    {
        "slug": "rag",
        "title": "RAG: retrieval-augmented generation",
        "category": "build",
        "became_usable_on": "2023-03-01",
        "date_note": (
            "The technique comes from a 2020 paper, so there is no launch day. Dated here "
            "to the cheap chat API that made it practical. LangChain's first release "
            "(Oct 2022) is an equally fair anchor."
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
            "A search box over years of meeting notes that answers the question you typed\n"
            "A study assistant that only knows your lecture slides"
        ),
        "before_this": (
            "You wrote FAQ pages by hand and hoped the wording matched what people typed. "
            "Anything smarter meant a keyword search engine and a team to tune synonyms, "
            "and even then a question spanning two documents went unanswered."
        ),
        "why_new": (
            "Search engines hand you files and leave the reading to you. When the answer "
            "sits half in one document and half in another, somebody has to open both and "
            "work it out. That reading is done by a machine now. It works on private "
            "material, on documents written last week, on anything that never went near a "
            "training set."
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
            "Boilerplate you never type: forms, API clients, config"
        ),
        "before_this": (
            "You searched Stack Overflow, adapted a stranger's snippet, and read library "
            "docs until the shape of the API was in your head. Autocomplete got you as far "
            "as the rest of a variable name."
        ),
        "why_new": (
            "Describe what you want in English and get code that runs. People who never "
            "learned to program ship small tools, and people who did work in languages "
            "they have never used."
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
            "A model that works in your actual repository. It reads files, edits them, "
            "runs the tests, and fixes what it broke."
        ),
        "what_you_can_build": (
            "A whole feature from a paragraph of description, delivered as a pull request\n"
            "A dependency upgrade across two hundred files\n"
            "A bug fix from nothing but a stack trace and a failing test\n"
            "A migration from one framework to another, done overnight"
        ),
        "before_this": (
            "You copied code out of a chat window, pasted it in, ran it, copied the error "
            "back, and repeated. Every loop needed a person to move text between two "
            "windows."
        ),
        "why_new": (
            "A model that can run the code sees whether it worked, so it retries without "
            "you. Work that used to take an afternoon of copy-paste gets handed over once, "
            "in full, across as many files as it touches."
        ),
    },
    {
        "slug": "mcp",
        "title": "MCP: the Model Context Protocol",
        "category": "infra",
        "became_usable_on": "2024-11-25",
        "resource_url": "https://modelcontextprotocol.io",
        "source_url": "https://www.anthropic.com/news/model-context-protocol",
        "one_liner": (
            "A standard plug shape for connecting AI assistants to tools and data. Write "
            "one connector per service and any assistant that speaks it can use it."
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
            "Nobody was going to write the same connector four times over, once per "
            "vendor, so niche systems stayed unconnected. Write it once against a shared "
            "protocol and it pays off everywhere, which is what makes the long tail worth "
            "building at all."
        ),
    },
    {
        "slug": "tool-use",
        "title": "Tool use: models that call your functions",
        "category": "agents",
        "became_usable_on": "2023-06-13",
        "resource_url": "https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview",
        "source_url": "https://openai.com/index/function-calling-and-other-api-updates/",
        "one_liner": (
            "You describe the functions a model is allowed to call; it decides when to call "
            "them and what to pass in, then uses the result."
        ),
        "what_you_can_build": (
            "An assistant that books the meeting rather than describing how to book it\n"
            "A support bot that looks up a real order status before answering\n"
            "A model that does arithmetic by calling a calculator instead of guessing\n"
            "Anything where the answer depends on live data the model cannot know"
        ),
        "before_this": (
            "Models could only produce text. To make one act, you parsed its output with "
            "regular expressions and hoped the format held. It broke constantly."
        ),
        "why_new": (
            "Everything that acts on your behalf runs on this. An assistant that books a "
            "table, files a ticket, or moves money is calling a function you defined, and "
            "until 2023 there was no dependable way to let it."
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
            "Hand the model a schema and get back JSON that matches it every time, ready "
            "to feed straight into the rest of your program."
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
            "A program cannot branch on a paragraph. Once the shape is guaranteed, an AI "
            "step sits in a pipeline like any other function call and the code around it "
            "stops needing a defensive wrapper."
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
            "thing land near each other. You search by meaning rather than by wording."
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
            "'Find things like this one' used to need a person to say what 'like' meant, "
            "category by category, and to keep saying it as the vocabulary moved. Now it "
            "is a distance calculation, and it runs over any pile of text you already have "
            "for a cost small enough to ignore."
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
            "Zapier has moved data between apps for a decade. The part it always handed "
            "back was the reading: is this a complaint, does this invoice look wrong, "
            "which of four people should see it. That step runs unattended now too."
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
            "Accurate transcription of ordinary speech, accents and background noise "
            "included, cheap enough to run on everything you record."
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
            "At a pound a minute you transcribed the one interview that mattered. At close "
            "to nothing you transcribe everything, and a year of meetings turns into an "
            "archive you can search."
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
            "Speech synthesis that sounds like a person, in any voice you have a short sample of."
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
            "Changing a line of narration is a text edit now rather than a booking, which "
            "is why one person on a laptop can put out dubbed courses and voiced games "
            "that used to need a budget and a booth."
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
            "Speech in, speech out, fast enough that you can cut in mid-sentence and it "
            "holds up as an actual phone conversation."
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
            "You can say something nobody planned for and still get an answer. Phone trees "
            "only ever walked the branches someone drew in advance, so the useful half of "
            "any call ended up with a person anyway."
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
            "Send an image and ask a question about it in plain language. There is no "
            "training step and no fixed list of things it can recognise."
        ),
        "what_you_can_build": (
            "A screenshot of a design turned into working front-end code\n"
            "Photos of a job site checked against a safety checklist\n"
            "A chart in a PDF read back as numbers\n"
            "Alt text for ten thousand images"
        ),
        "before_this": (
            "Computer vision meant collecting thousands of labelled examples and training a "
            "model per task. 'Is this shelf tidy?' was a research project."
        ),
        "why_new": (
            "The question does not have to be one anybody planned for. A classifier trained "
            "on shelf photos knows shelves; this will tell you the third box from the left "
            "is upside down, in a warehouse it has never seen, first time you ask."
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
            "Pull structured data out of PDFs, scans, and photos whatever the layout, with "
            "no per-vendor template to configure."
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
            "The first invoice from a new supplier works, with nobody having configured "
            "anything for it."
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
            "Stock libraries only hold pictures somebody already took. If what you had in "
            "mind was unusual, no budget and no amount of searching would turn it up. Now "
            "it gets made on request, in about ten seconds."
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
            "Change a photo by describing the change. Remove the bin, swap the background, "
            "extend the frame, without touching a selection tool."
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
            "Masking, cloning and relighting take years to do convincingly, and that, "
            "rather than the price of the software, is what kept photo editing a "
            "specialist trade. The edit is a sentence now."
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
            "A camera, a crew, a location and a schedule, or else an animator working for "
            "weeks. Even a five-second clip had a floor under it, in people and in days."
        ),
        "why_new": (
            "For a century there were two ways to make moving pictures: point a camera at "
            "something real, or draw every frame. There is a third now, and it costs little "
            "enough that you can try the idea before deciding whether to produce it."
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
            "Capable open-weight models that run on a laptop, with no API bill and nothing "
            "leaving the building."
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
            "A hospital, a law firm, a ship at sea: none of them could touch any of this "
            "while the only route was posting the data to someone else's server. The model "
            "runs where the data already is."
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
            "People who could never have trained a model can specialise one, for the price "
            "of a rented GPU and an afternoon."
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
            "Models that hold a whole book, codebase, or year of email in view at once, "
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
            "'Is this consistent throughout?' is not a question you can answer from "
            "excerpts. It needs the whole document in view at once, and that is an "
            "ordinary request now."
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
            "A model that looks at a screen and moves the mouse and keyboard, driving "
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
            "A great deal of office work lives in systems that expose nothing "
            "programmatically: the claims terminal from 1998, the supplier portal with no "
            "export button. For thirty years automation stopped at that wall. Everything "
            "on the far side of it stayed manual, or got a screen-scraping script that "
            "broke every quarter. A model that reads the screen and moves the mouse walks "
            "straight past it."
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
            "Five people can rate a hundred answers. Nobody can rate a hundred thousand of "
            "them again every time someone edits a prompt, which is why AI features shipped "
            "for years on spot-checks and nerve."
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
            "The person with the question can ask the follow-up themselves. A dashboard is "
            "frozen at the moment it was designed, so anything past it meant a specialist, "
            "a ticket, and three days."
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
            "Fake data used to mean obviously fake data. Anything with real variety in it "
            "had to be copied from real people, and it carried their risk into your "
            "staging database along with it."
        ),
    },
]
