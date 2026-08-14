import { useEffect, useRef } from "react";
import { Outlet, useNavigate, useRouterState } from "@tanstack/react-router";
import { useAtom } from "jotai";

import { AppShell } from "@/components/layout/app-shell";
import { ApiError } from "@/lib/api";
import { me } from "@/features/auth/api";
import { tokenAtom, userAtom } from "@/features/auth/state";

// The syllabus is public, and its detail routes are dynamic (/subjects/<slug>),
// so membership is a predicate rather than a set. /about is public for the same
// reason "/" is: it explains the list, so it has to be readable before signing in.
function isPublicPath(pathname: string) {
  return (
    pathname === "/" ||
    pathname === "/about" ||
    pathname === "/login" ||
    pathname.startsWith("/subjects/")
  );
}

function isFullBleedPath(pathname: string) {
  return isPublicPath(pathname) || pathname === "/onboarding";
}

export function AuthGate() {
  const [token, setToken] = useAtom(tokenAtom);
  const [user, setUser] = useAtom(userAtom);
  const navigate = useNavigate();
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const sessionExpiredFiredRef = useRef(false);

  useEffect(() => {
    if (!token || user) return;
    let cancelled = false;
    me()
      .then((u) => {
        if (!cancelled) setUser(u);
      })
      .catch((err) => {
        if (cancelled) return;
        if (err instanceof ApiError && err.status === 401) {
          setToken(null);
          setUser(null);
          sessionExpiredFiredRef.current = true;
        }
      });
    return () => {
      cancelled = true;
    };
  }, [token, user, setToken, setUser]);

  useEffect(() => {
    if (!token) {
      if (!isPublicPath(pathname)) navigate({ to: "/login" });
      return;
    }
    if (!user) return;
    // Opt-in onboarding gate: dormant while the backend reports onboarded=true
    // (template default). Activates once get_onboarded can return false. See CLAUDE.md.
    if (!user.onboarded && pathname !== "/onboarding") {
      navigate({ to: "/onboarding" });
      return;
    }
    // "/" is the public syllabus, so signed-in readers stay there; only the
    // auth-only screens bounce through to the dashboard.
    if (user.onboarded && (pathname === "/login" || pathname === "/onboarding")) {
      navigate({ to: "/dashboard" });
    }
  }, [token, user, pathname, navigate]);

  if (!token || !user || isFullBleedPath(pathname)) {
    return <Outlet />;
  }
  return <AppShell />;
}
