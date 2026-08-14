import { useQuery } from "@tanstack/react-query";

import {
  getEditorial,
  getSubject,
  listSubjects,
  type SubjectFilters,
} from "@/features/syllabus/api";

export function useSubjects(filters: SubjectFilters = {}) {
  return useQuery({
    queryKey: ["subjects", filters.category ?? "", filters.q ?? ""],
    queryFn: () => listSubjects(filters),
    staleTime: 5 * 60 * 1000,
  });
}

export function useSubject(slug: string) {
  return useQuery({
    queryKey: ["subject", slug],
    queryFn: () => getSubject(slug),
    staleTime: 5 * 60 * 1000,
  });
}

// The bar is module constants on the server: it can only change on deploy, so unlike
// the subject list there is nothing to go stale within a session.
export function useEditorial() {
  return useQuery({
    queryKey: ["editorial"],
    queryFn: getEditorial,
    staleTime: Infinity,
  });
}
