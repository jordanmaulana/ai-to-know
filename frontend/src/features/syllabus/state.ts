import { atom } from "jotai";

import { readProgress, writeProgress } from "@/features/syllabus/progress";
import type { ProgressMap, SubjectStatus } from "@/features/syllabus/types";

const progressBaseAtom = atom<ProgressMap>(
  typeof window === "undefined" ? {} : readProgress(),
);

/**
 * Read the whole map, write one slug at a time. The localStorage write lives
 * inside the setter so the atom and storage cannot drift apart.
 */
export const progressAtom = atom(
  (get) => get(progressBaseAtom),
  (get, set, slug: string, status: SubjectStatus) => {
    const next = { ...get(progressBaseAtom) };
    // "new" is the default, so clearing the key is how it is stored.
    if (status === "new") delete next[slug];
    else next[slug] = status;

    set(progressBaseAtom, next);
    writeProgress(next);
  },
);
