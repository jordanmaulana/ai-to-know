import { Link } from "@tanstack/react-router";

import { formatUsableOn } from "@/features/syllabus/format";
import type { Subject } from "@/features/syllabus/types";

export function SubjectCard({ subject, index }: { subject: Subject; index: number }) {
  const usableOn = formatUsableOn(subject.became_usable_on);

  return (
    <Link
      to="/subjects/$slug"
      params={{ slug: subject.slug }}
      style={{ animationDelay: `${Math.min(index, 12) * 28}ms` }}
      className="rise group flex h-full flex-col rounded-xl border border-rule bg-card p-5 transition-colors focus:outline-none focus-visible:border-accent focus-visible:bg-accent-soft hover:border-ink/20 hover:bg-accent-soft"
    >
      <p className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase">
        {subject.category_label}
      </p>

      <h3 className="font-display mt-3 text-lg leading-snug font-semibold text-ink">
        {subject.title}
      </h3>

      {/* mb keeps a floor under the gap; the footer's mt-auto absorbs the rest. */}
      <p className="mt-2 mb-5 line-clamp-3 text-[0.9375rem] leading-relaxed text-muted">
        {subject.one_liner}
      </p>

      <div className="mt-auto flex items-center justify-between gap-4 border-t border-rule pt-3">
        <span className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase tabular-nums">
          {usableOn}
        </span>
        <span
          aria-hidden
          className="text-accent opacity-0 transition-all duration-200 group-hover:translate-x-1 group-hover:opacity-100 group-focus-visible:opacity-100"
        >
          &rarr;
        </span>
      </div>
    </Link>
  );
}
