import { useEffect } from "react";
import { Link, createFileRoute } from "@tanstack/react-router";
import { Check, Minus } from "lucide-react";

import { SiteFooter } from "@/components/layout/site-footer";
import { SiteHeader } from "@/components/layout/site-header";
import { useEditorial } from "@/features/syllabus/hooks";

export const Route = createFileRoute("/about")({
  component: AboutPage,
});

function Eyebrow({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase">
      {children}
    </h2>
  );
}

function AboutPage() {
  // The bar itself is never restated here — it comes from syllabus/editorial.py, the
  // same text the crawler is judged against. Only the connective prose is written here.
  const { data: editorial, isPending, isError } = useEditorial();

  useEffect(() => {
    document.title = "How this works — AI to know";
  }, []);

  return (
    <div className="min-h-full bg-paper text-ink">
      <SiteHeader width="prose" />

      <main className="mx-auto max-w-3xl px-6 pt-14 pb-20">
        <article className="rise">
          <Eyebrow>How this works</Eyebrow>

          <h1 className="font-display mt-5 text-4xl leading-[1.08] font-semibold tracking-tight text-balance sm:text-5xl">
            A short list of things that became possible.
          </h1>

          <div className="mt-6 space-y-5 text-lg leading-relaxed text-ink/80">
            <p>
              Most writing about AI is news. Something launched, someone raised
              money. It arrives constantly and tells you almost nothing about what
              you can do this year that you couldn&rsquo;t do last year.
            </p>
            <p>
              This is the other list. Every entry is a capability described in
              general rather than a product with a logo: one thing an ordinary
              person can do that had no practical route before. The list is short
              and it grows slowly.
            </p>
            <p>
              Nothing here needs mastering. Knowing that a thing exists, and what it
              replaced, is enough to recognise the moment you need it.
            </p>
          </div>

          {/* The bar. Everything below this line is served from the same file the
              crawler reads, so the public rules and the enforced rules cannot drift. */}
          <section className="mt-16">
            <Eyebrow>What earns a place</Eyebrow>

            {isPending && (
              <p className="mt-4 font-mono text-xs tracking-widest text-muted uppercase">
                Loading&hellip;
              </p>
            )}

            {isError && (
              <p className="mt-4 text-sm text-muted">
                The rules didn&rsquo;t load.{" "}
                <Link to="/" className="text-accent underline underline-offset-4">
                  Back to the list
                </Link>
                .
              </p>
            )}

            {editorial && (
              <>
                <p className="font-display mt-5 text-2xl leading-snug font-semibold text-balance">
                  {editorial.bar}
                </p>

                <div className="mt-8 rounded-xl border border-rule bg-card p-6 sm:p-8">
                  <div className="grid gap-2 sm:grid-cols-[5rem_1fr] sm:gap-6">
                    <h3 className="font-mono text-[0.6875rem] tracking-widest text-accent uppercase sm:pt-1">
                      In
                    </h3>
                    <ul className="space-y-3">
                      {editorial.qualifies.map((item) => (
                        <li key={item} className="flex gap-3 leading-relaxed">
                          <Check
                            className="mt-1 h-4 w-4 shrink-0 text-accent"
                            aria-hidden
                          />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="my-6 h-px bg-rule" aria-hidden />

                  <div className="grid gap-2 sm:grid-cols-[5rem_1fr] sm:gap-6">
                    <h3 className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase sm:pt-1">
                      Out
                    </h3>
                    <ul className="flex flex-wrap gap-2">
                      {editorial.disqualifies.map((item) => (
                        <li
                          key={item}
                          className="flex items-center gap-1.5 rounded-full border border-rule px-3 py-1 text-sm text-muted"
                        >
                          <Minus className="h-3 w-3 shrink-0" aria-hidden />
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <p className="mt-5 text-sm leading-relaxed text-muted">
                  That is why there is no entry for a new model. A better model is
                  worth reading about, but the list of things you can make stays the
                  same length.
                </p>
              </>
            )}
          </section>

          {editorial && (
            <section className="mt-16">
              <Eyebrow>How to read an entry</Eyebrow>
              <p className="mt-4 leading-relaxed text-muted">
                Every entry answers the same three questions, in the same order.
              </p>
              <ol className="mt-6 divide-y divide-rule border-y border-rule">
                {editorial.three_questions.map(({ question, note }, index) => (
                  <li key={question} className="flex gap-4 py-4">
                    <span className="font-mono text-[0.6875rem] tracking-widest text-accent tabular-nums">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <div>
                      <p className="font-medium">{question}</p>
                      <p className="mt-1 text-sm leading-relaxed text-muted">{note}</p>
                    </div>
                  </li>
                ))}
              </ol>
            </section>
          )}

          <section className="mt-16">
            <Eyebrow>How entries get here</Eyebrow>
            <ol className="mt-6 space-y-4">
              {[
                "Once a day, the Hacker News front page is pulled in.",
                "A free filter drops anything off-topic or below the points floor.",
                "Whatever survives is read once against the bar above, the same words you just read, judged by a model.",
                "Anything that passes is filed as a draft, and a draft is not published.",
                "A person reads the draft and publishes it, or doesn't.",
              ].map((step, index) => (
                <li key={step} className="flex gap-4 leading-relaxed">
                  <span className="mt-0.5 font-mono text-[0.6875rem] tracking-widest text-muted tabular-nums">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span>{step}</span>
                </li>
              ))}
            </ol>
            <p className="mt-6 text-sm leading-relaxed text-muted">
              Most days nothing is published. A list that grew every morning would
              just be news again.
            </p>
          </section>

          {editorial && (
            <section className="mt-16">
              <Eyebrow>Categories</Eyebrow>
              <p className="mt-4 leading-relaxed text-muted">
                Entries are filed by what they let you do.
              </p>
              <dl className="mt-6 divide-y divide-rule border-y border-rule">
                {editorial.categories.map((category) => (
                  <div
                    key={category.slug}
                    className="grid gap-1 py-4 sm:grid-cols-[10rem_1fr] sm:gap-6"
                  >
                    <dt className="font-medium">{category.label}</dt>
                    <dd className="leading-relaxed text-muted">{category.note}</dd>
                  </div>
                ))}
              </dl>
            </section>
          )}

          {/* No top rule: the section above already closes on one, and stacking both
              reads as a stutter. */}
          <div className="mt-12">
            <Link
              to="/"
              className="inline-flex items-center gap-2 rounded-full bg-ink px-4 py-2 font-mono text-[0.6875rem] tracking-widest text-paper uppercase transition-opacity hover:opacity-85"
            >
              See the list
            </Link>
          </div>
        </article>
      </main>

      <SiteFooter width="prose" />
    </div>
  );
}
