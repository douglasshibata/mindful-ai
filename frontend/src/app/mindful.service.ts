import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

export interface MoodLog {
  id?: number;
  user_id?: number;
  mood_score: number;
  anxiety_score?: number;
  anxiety_level?: number;
  sleep_hours?: number;
  triggers?: string;
  notes?: string;
  timestamp?: string;
  recorded_at?: string;
}

export interface CrisisHelpline {
  name: string;
  phone: string;
  available: string;
  country: string;
}

export interface CognitiveReframingData {
  automatic_thought: string;
  detected_distortions: string[];
  rational_counter_evidence: string;
  alternative_thought: string;
  actionable_grounding_step: string;
}

export interface ThoughtChallengeResult {
  status: 'SUCCESS' | 'CRISIS_DETECTED';
  distortions?: string;
  evidence_against?: string;
  balanced_thought?: string;
  grounding_step?: string;
  data?: {
    is_crisis?: boolean;
    message?: string;
    helplines?: CrisisHelpline[];
    automatic_thought?: string;
    detected_distortions?: string[];
    rational_counter_evidence?: string;
    alternative_thought?: string;
    actionable_grounding_step?: string;
  };
}

export interface MoodTrendSummary {
  total_logs: number;
  average_mood: number;
  average_anxiety: number;
  average_sleep_hours?: number;
  dominant_triggers: string[];
  recommendation: string;
}

@Injectable({
  providedIn: 'root'
})
export class MindfulService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  logMood(log: MoodLog): Observable<MoodLog> {
    return this.http.post<MoodLog>(`${this.apiUrl}/mood`, log);
  }

  getMoodLogs(): Observable<MoodLog[]> {
    return this.http.get<MoodLog[]>(`${this.apiUrl}/mood`);
  }

  getTrends(): Observable<MoodTrendSummary> {
    return this.http.get<MoodTrendSummary>(`${this.apiUrl}/api/v1/trends`);
  }

  challengeThought(thought: string, intensityBefore: number = 7): Observable<ThoughtChallengeResult> {
    return this.http.post<ThoughtChallengeResult>(`${this.apiUrl}/challenge-thought`, {
      thought,
      intensity_before: intensityBefore
    });
  }
}
