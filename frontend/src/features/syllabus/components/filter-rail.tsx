import { Search } from "lucide-react";

import { cn } from "@/lib/utils";
import { CATEGORIES } from "@/features/syllabus/types";

interface FilterRailProps {
  category: string;
  onCategoryChange: (category: string) => void;
  query: string;
  onQueryChange: (query: string) => void;
  /** Subjects per category slug; the empty key holds the total. */
  counts: Record<string, number>;
}

export function FilterRail({
  category,
  onCategoryChange,
  query,
  onQueryChange,
  counts,
}: FilterRailProps) {
  const options = [{ slug: "", label: "Everything" }, ...CATEGORIES];

  return (
    <div className="sticky top-0 z-10 border-y border-rule bg-paper/90 px-6 py-3 backdrop-blur">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-1 gap-y-2">
        {options.map((option) => {
          const active = category === option.slug;
          return (
            <button
              key={option.slug || "all"}
              type="button"
              onClick={() => onCategoryChange(option.slug)}
              className={cn(
                "flex items-center gap-1.5 rounded-full px-3 py-1.5 font-mono text-[0.6875rem] tracking-widest uppercase transition-colors",
                active ? "bg-ink text-paper" : "text-muted hover:bg-rule/60 hover:text-ink",
              )}
            >
              {option.label}
              <span
                className={cn(
                  "tabular-nums",
                  active ? "text-paper/55" : "text-muted/60",
                )}
              >
                {counts[option.slug] ?? 0}
              </span>
            </button>
          );
        })}

        <label className="mt-1 flex w-full items-center gap-2 border-b border-rule pb-1 focus-within:border-accent sm:mt-0 sm:ml-auto sm:w-auto">
          <Search className="h-3.5 w-3.5 shrink-0 text-muted" aria-hidden />
          <span className="sr-only">Search capabilities</span>
          <input
            value={query}
            onChange={(event) => onQueryChange(event.target.value)}
            placeholder="Search"
            className="w-full min-w-0 bg-transparent font-mono text-xs text-ink placeholder:text-muted focus:outline-none sm:w-40"
          />
        </label>
      </div>
    </div>
  );
}
