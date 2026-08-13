import { useEffect, useMemo, useState } from "react";
import { createFileRoute } from "@tanstack/react-router";

import { FilterRail } from "@/features/syllabus/components/filter-rail";
import { SubjectCard } from "@/features/syllabus/components/subject-card";
import { useSubjects } from "@/features/syllabus/hooks";
import { CATEGORIES } from "@/features/syllabus/types";

export const Route = createFileRoute("/")({
  component: SyllabusPage,
});

function SyllabusPage() {
  const [category, setCategory] = useState("");
  const [query, setQuery] = useState("");

  // One fetch for the whole list: the chip counts have to cover every category,
  // not just the active one, and filtering ~20 rows locally beats a round-trip.
  const { data: subjects, isPending, isError } = useSubjects();

  const counts = useMemo(() => {
    const tally: Record<string, number> = { "": subjects?.length ?? 0 };
    for (const { slug } of CATEGORIES) tally[slug] = 0;
    for (const subject of subjects ?? []) tally[subject.category] += 1;
    return tally;
  }, [subjects]);

  const visible = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return (subjects ?? []).filter((subject) => {
      if (category && subject.category !== category) return false;
      if (!needle) return true;
      return (
        subject.title.toLowerCase().includes(needle) ||
        subject.one_liner.toLowerCase().includes(needle)
      );
    });
  }, [subjects, category, query]);

  const total = subjects?.length ?? 0;

  useEffect(() => {
    if (total) document.title = `${total} things to know — AI to know`;
  }, [total]);

  return (
    <div className="min-h-full bg-paper text-ink">
      <header className="border-b border-rule">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <span className="font-mono text-xs tracking-[0.2em] uppercase">
            ai&#8202;/&#8202;to&#8202;know
          </span>
          <span className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase">
            a running list
          </span>
        </div>
      </header>

      <section className="mx-auto max-w-6xl px-6 pt-12 pb-8 sm:pt-14">
        <h1 className="font-display max-w-3xl text-3xl leading-[1.1] font-semibold tracking-tight text-balance sm:text-4xl">
          You don&rsquo;t have to master any of this. You just have to know what it
          lets you <span className="text-accent">do now</span>.
        </h1>
        <p className="mt-4 max-w-2xl text-[0.9375rem] leading-relaxed text-muted">
          A plain-English list of things that became possible recently. Each entry
          says what it is, what you can make with it, and what you had to do
          instead before it existed.
        </p>
      </section>

      <FilterRail
        category={category}
        onCategoryChange={setCategory}
        query={query}
        onQueryChange={setQuery}
        counts={counts}
      />

      <main className="mx-auto max-w-6xl px-6 pb-24">
        {isPending && (
          <p className="py-16 font-mono text-xs tracking-widest text-muted uppercase">
            Loading&hellip;
          </p>
        )}

        {isError && (
          <p className="py-16 text-sm text-ink">
            The list didn&rsquo;t load. Refresh the page to try again.
          </p>
        )}

        {!isPending && !isError && visible.length === 0 && (
          <div className="py-16">
            <p className="font-display text-xl font-semibold">Nothing matches that.</p>
            <p className="mt-2 text-sm text-muted">
              Try a broader word, or clear the filters to see everything.
            </p>
          </div>
        )}

        {visible.length > 0 && (
          <>
            <div className="grid gap-4 pt-8 sm:grid-cols-2 lg:grid-cols-3">
              {visible.map((subject, index) => (
                <SubjectCard key={subject.slug} subject={subject} index={index} />
              ))}
            </div>
            <p className="mt-10 border-t border-rule pt-6 font-mono text-[0.6875rem] tracking-widest text-muted uppercase">
              {visible.length === total
                ? `${total} ${total === 1 ? "capability" : "capabilities"}`
                : `${visible.length} of ${total}`}
            </p>
          </>
        )}
      </main>
    </div>
  );
}
