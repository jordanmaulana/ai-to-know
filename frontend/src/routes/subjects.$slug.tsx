import { useEffect } from "react";
import { Link, createFileRoute } from "@tanstack/react-router";
import { useAtom } from "jotai";
import { ArrowUpRight } from "lucide-react";

import { SiteFooter } from "@/components/layout/site-footer";
import { SiteHeader } from "@/components/layout/site-header";
import { StatusSelect } from "@/features/syllabus/components/status-select";
import { formatUsableOn } from "@/features/syllabus/format";
import { useSubject } from "@/features/syllabus/hooks";
import { progressAtom } from "@/features/syllabus/state";

export const Route = createFileRoute("/subjects/$slug")({
  component: SubjectPage,
});

function SubjectPage() {
  const { slug } = Route.useParams();
  const { data: subject, isPending, isError } = useSubject(slug);
  const [progress, setStatus] = useAtom(progressAtom);

  useEffect(() => {
    if (subject) document.title = `${subject.title} — AI to know`;
  }, [subject]);

  return (
    <div className="min-h-full bg-paper text-ink">
      <SiteHeader width="prose" />

      <main className="mx-auto max-w-3xl px-6 pt-14 pb-20">
        {isPending && (
          <p className="font-mono text-xs tracking-widest text-muted uppercase">
            Loading&hellip;
          </p>
        )}

        {isError && (
          <div>
            <h1 className="font-display text-3xl font-semibold">Not on the list</h1>
            <p className="mt-3 text-sm text-muted">
              Nothing is published at that address.{" "}
              <Link to="/" className="text-accent underline underline-offset-4">
                Back to everything
              </Link>
              .
            </p>
          </div>
        )}

        {subject && (
          <article className="rise">
            <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-4">
              <p className="flex flex-wrap items-center gap-x-3 gap-y-1 font-mono text-[0.6875rem] tracking-widest text-muted uppercase">
                <span>{subject.category_label}</span>
                {formatUsableOn(subject.became_usable_on) && (
                  <>
                    <span className="text-rule" aria-hidden>
                      /
                    </span>
                    <span>Usable {formatUsableOn(subject.became_usable_on)}</span>
                  </>
                )}
              </p>

              {/* Personal, browser-local: the syllabus API is read-only for everyone. */}
              <StatusSelect
                status={progress[slug] ?? "new"}
                onChange={(next) => setStatus(slug, next)}
                subjectTitle={subject.title}
              />
            </div>

            <h1 className="font-display mt-5 text-4xl leading-[1.08] font-semibold tracking-tight text-balance sm:text-5xl">
              {subject.title}
            </h1>

            <p className="mt-6 max-w-2xl text-lg leading-relaxed text-ink/80">
              {subject.one_liner}
            </p>

            {/* Only present when the date is a judgement call, so the reader knows not to
                read it as a launch day. Most entries render nothing here. */}
            {subject.date_note && (
              <p className="mt-4 max-w-2xl border-l-2 border-rule pl-4 text-sm leading-relaxed text-muted">
                {subject.date_note}
              </p>
            )}

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

      <SiteFooter width="prose" />
    </div>
  );
}
