import { useEffect } from "react";
import { Link, createFileRoute } from "@tanstack/react-router";
import { ArrowLeft, ArrowUpRight } from "lucide-react";

import { useSubject } from "@/features/syllabus/hooks";

export const Route = createFileRoute("/subjects/$slug")({
  component: SubjectPage,
});

function SubjectPage() {
  const { slug } = Route.useParams();
  const { data: subject, isPending, isError } = useSubject(slug);

  useEffect(() => {
    if (subject) document.title = `${subject.title} — AI to know`;
  }, [subject]);

  return (
    <div className="min-h-full bg-paper text-ink">
      <header className="border-b border-rule">
        <div className="mx-auto flex max-w-3xl items-center justify-between px-6 py-5">
          <Link
            to="/"
            className="flex items-center gap-2 font-mono text-xs tracking-widest text-muted uppercase transition-colors hover:text-ink"
          >
            <ArrowLeft className="h-3.5 w-3.5" aria-hidden />
            All capabilities
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-6 pt-14 pb-24">
        {isPending && (
          <p className="font-mono text-xs tracking-widest text-muted uppercase">
            Loading&hellip;
          </p>
        )}

        {isError && (
          <div>
            <h1 className="font-display text-3xl font-semibold">Not on the list</h1>
            <p className="mt-3 text-sm text-muted">
              This capability either moved or was never published.{" "}
              <Link to="/" className="text-accent underline underline-offset-4">
                Back to everything
              </Link>
              .
            </p>
          </div>
        )}

        {subject && (
          <article className="rise">
            <p className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase">
              {subject.category_label}
            </p>

            <h1 className="font-display mt-5 text-4xl leading-[1.08] font-semibold tracking-tight text-balance sm:text-5xl">
              {subject.title}
            </h1>

            <p className="mt-6 max-w-2xl text-lg leading-relaxed text-ink/80">
              {subject.one_liner}
            </p>

            {/* The hinge: the whole point of the entry is this before/after pair. */}
            <section
              aria-label="What changed"
              className="mt-12 rounded-xl border border-rule bg-card p-6 sm:p-8"
            >
              <div className="grid gap-2 sm:grid-cols-[5rem_1fr] sm:gap-6">
                <h2 className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase sm:pt-1">
                  Before
                </h2>
                <p className="leading-relaxed text-muted">{subject.before_this}</p>
              </div>

              <div className="my-6 h-px bg-rule" aria-hidden />

              <div className="grid gap-2 sm:grid-cols-[5rem_1fr] sm:gap-6">
                <h2 className="font-mono text-[0.6875rem] tracking-widest text-accent uppercase sm:pt-1">
                  Now
                </h2>
                <p className="leading-relaxed text-ink">{subject.why_new}</p>
              </div>
            </section>

            <section className="mt-12">
              <h2 className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase">
                What you can make
              </h2>
              <ul className="mt-4 divide-y divide-rule border-y border-rule">
                {subject.what_you_can_build.map((item) => (
                  <li key={item} className="flex gap-4 py-3.5">
                    <span className="mt-2.5 h-1.5 w-1.5 shrink-0 rounded-full bg-accent" aria-hidden />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </section>

            {(subject.resource_url || subject.source_url) && (
              <section className="mt-10 flex flex-wrap gap-3">
                {subject.resource_url && (
                  <a
                    href={subject.resource_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-2 rounded-full bg-ink px-4 py-2 font-mono text-[0.6875rem] tracking-widest text-paper uppercase transition-opacity hover:opacity-85"
                  >
                    Start here
                    <ArrowUpRight className="h-3.5 w-3.5" aria-hidden />
                  </a>
                )}
                {subject.source_url && (
                  <a
                    href={subject.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-2 rounded-full border border-rule px-4 py-2 font-mono text-[0.6875rem] tracking-widest text-muted uppercase transition-colors hover:text-ink"
                  >
                    Source
                    <ArrowUpRight className="h-3.5 w-3.5" aria-hidden />
                  </a>
                )}
              </section>
            )}
          </article>
        )}
      </main>
    </div>
  );
}
