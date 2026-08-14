import { Link, useRouterState } from "@tanstack/react-router";

import { cn } from "@/lib/utils";

const NAV = [
  { to: "/", label: "The list" },
  { to: "/about", label: "How this works" },
] as const;

// A subject page is part of the list, not a third place — keep "The list" lit there
// so a reader deep in an entry can still see where they are.
function isActive(navPath: string, pathname: string) {
  if (navPath === "/") return pathname === "/" || pathname.startsWith("/subjects/");
  return pathname === navPath;
}

/**
 * The public counterpart to AppShell's sidebar. Used by every screen a signed-out
 * reader can reach; the authenticated dashboard keeps its own chrome.
 */
export function SiteHeader({ width = "wide" }: { width?: "wide" | "prose" }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <header className="border-b border-rule">
      <div
        className={cn(
          "mx-auto flex items-center justify-between gap-6 px-6 py-5",
          width === "prose" ? "max-w-3xl" : "max-w-6xl",
        )}
      >
        <Link
          to="/"
          className="font-mono text-xs tracking-[0.2em] uppercase transition-colors hover:text-accent"
        >
          ai&#8202;/&#8202;to&#8202;know
        </Link>

        <nav className="flex items-center gap-5 sm:gap-6">
          {NAV.map((item) => {
            const active = isActive(item.to, pathname);
            return (
              <Link
                key={item.to}
                to={item.to}
                aria-current={active ? "page" : undefined}
                className={cn(
                  "font-mono text-[0.6875rem] tracking-widest whitespace-nowrap uppercase transition-colors",
                  active ? "text-ink" : "text-muted hover:text-ink",
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
