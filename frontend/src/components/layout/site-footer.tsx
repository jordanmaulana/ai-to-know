import { ArrowUpRight, Heart } from "lucide-react";

import { cn } from "@/lib/utils";

const SPONSOR_URL = "https://github.com/sponsors/jordanmaulana";
const AUTHOR_URL = "https://jordanmaulana.space";

/**
 * Closes every public page. Takes the same `width` as SiteHeader so the rule above
 * and the rule below line up on the same gutter.
 */
export function SiteFooter({ width = "wide" }: { width?: "wide" | "prose" }) {
  return (
    <footer className="border-t border-rule">
      <div
        className={cn(
          "mx-auto flex flex-col gap-6 px-6 py-12 sm:flex-row sm:items-center sm:justify-between",
          width === "prose" ? "max-w-3xl" : "max-w-6xl",
        )}
      >
        <div className="flex max-w-md flex-col gap-3">
          <p className="text-sm leading-relaxed text-muted">
            Keeping this list current means reading the Hacker News front page every day
            and paying a model to judge what is actually new. That bill is real, and one
            person pays it.
          </p>

          <p className="font-mono text-[0.6875rem] tracking-widest text-muted uppercase">
            Built by{" "}
            <a
              href={AUTHOR_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 text-ink transition-colors hover:text-accent"
            >
              jordanmaulana.space
              <ArrowUpRight className="h-3 w-3" aria-hidden />
            </a>
          </p>
        </div>

        <a
          href={SPONSOR_URL}
          target="_blank"
          rel="noreferrer"
          className="inline-flex shrink-0 items-center gap-2 self-start rounded-full bg-ink px-4 py-2 font-mono text-[0.6875rem] tracking-widest text-paper uppercase transition-opacity hover:opacity-85"
        >
          <Heart className="h-3.5 w-3.5" aria-hidden />
          Support this list
          <ArrowUpRight className="h-3.5 w-3.5" aria-hidden />
        </a>
      </div>
    </footer>
  );
}
