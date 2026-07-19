/**
 * Shared TypeScript types matching the API response schemas.
 */

export interface Scan {
  id: string;
  target_url: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  profile: string;
  overall_score: number | null;
  overall_grade: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface Finding {
  id: string;
  owasp_id: string;
  owasp_name: string;
  dimension: string;
  passed: boolean;
  severity: 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  title: string;
  description: string;
  business_impact: string;
  recommendation: string;
  effort: string;
  evidence: Record<string, unknown>;
  references: string[];
}

export interface DimensionScore {
  id: string;
  dimension: string;
  score: number;
  weight: number;
  grade: string;
  label: string;
}

export interface ScanDetail extends Scan {
  findings: Finding[];
  dimension_scores: DimensionScore[];
}

export interface DashboardStats {
  total_scans: number;
  average_score: number;
}

export interface ApiKey {
  id: string;
  name: string;
  key?: string; // Only present on creation
  last_used_at: string | null;
}
