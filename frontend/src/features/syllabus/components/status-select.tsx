import { ChevronDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { STATUS_OPTIONS } from "@/features/syllabus/types";
import type { SubjectStatus } from "@/features/syllabus/types";

// Complete literal strings — Tailwind never sees a class assembled from a variable.
const PILL: Record<SubjectStatus, string> = {
  new: "border-rule bg-card text-muted hover:border-ink/20 hover:text-ink",
  practicing: "border-accent/40 bg-accent-soft text-accent",
  tried: "border-accent/40 bg-accent-soft text-accent",
  mastered: "border-ink bg-ink text-paper",
};

interface StatusSelectProps {
  status: SubjectStatus;
  onChange: (status: SubjectStatus) => void;
  /** Names the control for screen readers, since its only visible text is the value. */
  subjectTitle: string;
}

export function StatusSelect({ status, onChange, subjectTitle }: StatusSelectProps) {
  return (
    // The pill is the label, not the select: clicking anywhere in the padding still
    // opens the picker, and the chevron inherits the current state's colour.
    <label
      className={cn(
        "relative inline-flex cursor-pointer items-center rounded-full border py-2 pr-9 pl-4 font-mono text-[0.6875rem] tracking-widest uppercase transition-colors focus-within:border-accent focus-within:ring-2 focus-within:ring-accent/25",
        PILL[status],
      )}
    >
      <span className="sr-only">Your progress on {subjectTitle}</span>
      <select
        value={status}
        onChange={(event) => onChange(event.target.value as SubjectStatus)}
        // uppercase is repeated here: Chrome draws the closed select's text in a
        // shadow slot that does not pick up the label's text-transform.
        className="cursor-pointer appearance-none bg-transparent uppercase focus:outline-none"
      >
        {STATUS_OPTIONS.map((option) => (
          // The popup is drawn by the OS; these two classes are the only part of it
          // browsers honour, and they keep the list readable under the dark pill.
          <option key={option.value} value={option.value} className="bg-card text-ink">
            {option.label}
          </option>
        ))}
      </select>
      <ChevronDown
        className="pointer-events-none absolute right-3.5 h-3.5 w-3.5"
        aria-hidden
      />
    </label>
  );
}
