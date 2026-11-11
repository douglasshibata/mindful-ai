import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MindfulService, MoodLog, ThoughtChallengeResult, MoodTrendSummary } from './mindful.service';
import { BreathingComponent } from './components/breathing/breathing.component';
import { CrisisNotificationService } from './core/crisis-notification.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, BreathingComponent],
  template: `
    <div class="min-h-screen bg-slate-50 p-6 md:p-10 font-sans text-slate-800">
      <!-- Top Emergency Crisis Banner / Modal -->
      <div *ngIf="crisisState().isActive" class="max-w-4xl mx-auto mb-8 bg-red-600 text-white p-6 rounded-2xl shadow-xl border-2 border-red-700 animate-pulse">
        <div class="flex items-start justify-between">
          <div>
            <h2 class="text-2xl font-bold flex items-center gap-2">
              <span>🚨</span> Suporte Clínico e Apoio Imediato
            </h2>
            <p class="mt-2 text-red-100 text-base leading-relaxed">
              {{ crisisState().message }}
            </p>
          </div>
          <button (click)="dismissCrisis()" class="text-white hover:text-red-200 text-2xl font-bold px-2">✕</button>
        </div>

        <div class="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-red-400">
          <div *ngFor="let h of crisisState().helplines" class="bg-red-700/80 p-3 rounded-xl">
            <p class="font-bold text-white text-sm">{{ h.name }}</p>
            <p class="text-2xl font-extrabold text-amber-300 mt-1">{{ h.phone }}</p>
            <p class="text-xs text-red-200">{{ h.available }} ({{ h.country }})</p>
          </div>
        </div>
      </div>

      <header class="mb-10 text-center">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-100 text-teal-800 text-xs font-semibold mb-3">
          <span>🧠</span> Clinical Wellness & Cognitive Companion v2.0
        </div>
        <h1 class="text-4xl font-extrabold text-teal-700 tracking-tight">MindfulAI</h1>
        <p class="text-slate-600 mt-2 max-w-xl mx-auto">
          Práticas de autorregulação emocional, reestruturação cognitiva empírica (TCC) e proteção clínica ativa.
        </p>
      </header>

      <main class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Mood & Anxiety Tracker Section -->
        <section class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
          <div>
            <h2 class="text-xl font-bold mb-4 text-slate-800 flex items-center gap-2">
              <span>📊</span> Registro Diário de Bem-Estar
            </h2>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-sm font-medium text-slate-700 mb-1">
                  <span>Humor Geral (1-10)</span>
                  <span class="text-teal-600 font-bold">{{ currentMood.mood_score }}</span>
                </div>
                <input type="range" min="1" max="10" [(ngModel)]="currentMood.mood_score" class="w-full h-2 bg-teal-100 rounded-lg appearance-none cursor-pointer accent-teal-600">
              </div>

              <div>
                <div class="flex justify-between text-sm font-medium text-slate-700 mb-1">
                  <span>Nível de Ansiedade (1-10)</span>
                  <span class="text-rose-600 font-bold">{{ currentMood.anxiety_score }}</span>
                </div>
                <input type="range" min="1" max="10" [(ngModel)]="currentMood.anxiety_score" class="w-full h-2 bg-rose-100 rounded-lg appearance-none cursor-pointer accent-rose-600">
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Gatilhos Recorrentes</label>
                <input type="text" [(ngModel)]="currentMood.triggers" placeholder="Ex: Trabalho, Prazos, Família, Sono" class="w-full text-sm border-slate-300 rounded-lg shadow-sm focus:ring-teal-500 focus:border-teal-500 p-2.5 border">
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Notas Sensíveis (Criptografadas AES-256)</label>
                <textarea [(ngModel)]="currentMood.notes" placeholder="Descreva sentimentos ou contexto..." class="w-full text-sm border-slate-300 rounded-lg shadow-sm focus:ring-teal-500 focus:border-teal-500 p-2.5 border" rows="3"></textarea>
              </div>
            </div>
          </div>

          <div class="mt-6">
            <button (click)="saveMood()" class="w-full bg-teal-600 text-white font-medium py-2.5 rounded-xl hover:bg-teal-700 transition shadow-sm">
              Salvar Registro Seguro
            </button>
            <p *ngIf="trendSummary" class="text-xs text-slate-500 mt-3 italic text-center">
              Média do Humor: {{ trendSummary.average_mood }} | Ansiedade: {{ trendSummary.average_anxiety }} ({{ trendSummary.total_logs }} registros)
            </p>
          </div>
        </section>

        <!-- CBT Thought Challenger -->
        <section class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
          <div>
            <h2 class="text-xl font-bold mb-4 text-slate-800 flex items-center gap-2">
              <span>💡</span> Questionamento Cognitivo (TCC)
            </h2>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Qual pensamento automático disfuncional surgiu?</label>
                <textarea [(ngModel)]="negativeThought" placeholder="Ex: Eu nunca vou dar conta disso, sou um fracasso completo..." class="w-full text-sm border-slate-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 p-2.5 border" rows="3"></textarea>
              </div>

              <button (click)="challenge()" [disabled]="loading" class="w-full bg-indigo-600 text-white font-medium py-2.5 rounded-xl hover:bg-indigo-700 transition disabled:opacity-50 shadow-sm flex items-center justify-center gap-2">
                <span>{{ loading ? 'Analisando clinicamente...' : 'Desafiar Pensamento' }}</span>
              </button>
            </div>

            <!-- Structured CBT Result -->
            <div *ngIf="structuredResult" class="mt-6 p-4 bg-indigo-50/60 rounded-xl border border-indigo-100 text-sm space-y-3">
              <h3 class="font-bold text-indigo-900 text-base">Reenquadramento Cognitivo Estruturado:</h3>

              <div>
                <span class="font-semibold text-slate-700">Distorções Identificadas:</span>
                <div class="flex flex-wrap gap-1.5 mt-1">
                  <span *ngFor="let d of getDistortionsList()" class="px-2 py-0.5 bg-indigo-200 text-indigo-800 rounded-md text-xs font-medium">
                    {{ d }}
                  </span>
                </div>
              </div>

              <div>
                <span class="font-semibold text-slate-700">Evidências Contrárias:</span>
                <p class="text-slate-600 mt-0.5">{{ structuredResult.rational_counter_evidence || structuredResult.evidence_against }}</p>
              </div>

              <div>
                <span class="font-semibold text-slate-700">Perspectiva Equilibrada:</span>
                <p class="text-indigo-950 font-medium italic mt-0.5">
                  "{{ structuredResult.alternative_thought || structuredResult.balanced_thought }}"
                </p>
              </div>

              <div *ngIf="structuredResult.actionable_grounding_step || structuredResult.grounding_step" class="p-2.5 bg-white rounded-lg border border-indigo-100 text-xs text-indigo-900">
                <strong>Ação Somática Recomendada:</strong> {{ structuredResult.actionable_grounding_step || structuredResult.grounding_step }}
              </div>
            </div>
          </div>

          <p class="text-xs text-slate-400 mt-4 text-center">
            Filtragem determinística ativa contra ideação de risco e automutilação.
          </p>
        </section>
      </main>

      <!-- Breathing Exercise Pacer -->
      <div class="max-w-5xl mx-auto mt-10">
        <app-breathing></app-breathing>
      </div>

      <footer class="mt-14 text-center text-slate-400 text-xs">
        MindfulAI é uma ferramenta clínica complementar baseada em TCC e não substitui o diagnóstico ou tratamento médico/psicológico. Em caso de crise, disque 188 (CVV).
      </footer>
    </div>
  `,
  styles: []
})
export class AppComponent implements OnInit {
  currentMood: MoodLog = { mood_score: 5, anxiety_score: 5, notes: '', triggers: '' };
  negativeThought: string = '';
  structuredResult: any = null;
  loading: boolean = false;
  trendSummary: MoodTrendSummary | null = null;

  readonly crisisState = this.crisisService.crisisState;

  constructor(
    private mindfulService: MindfulService,
    private crisisService: CrisisNotificationService
  ) {}

  ngOnInit() {
    this.loadTrends();
  }

  loadTrends() {
    this.mindfulService.getTrends().subscribe({
      next: (t) => { this.trendSummary = t; },
      error: () => {}
    });
  }

  saveMood() {
    this.mindfulService.logMood(this.currentMood).subscribe({
      next: () => {
        alert('Registro de bem-estar gravado com criptografia em repouso.');
        this.currentMood = { mood_score: 5, anxiety_score: 5, notes: '', triggers: '' };
        this.loadTrends();
      },
      error: (err) => console.error(err)
    });
  }

  dismissCrisis() {
    this.crisisService.dismissAlert();
  }

  challenge() {
    if (!this.negativeThought.trim()) return;
    this.loading = true;

    this.mindfulService.challengeThought(this.negativeThought).subscribe({
      next: (res: ThoughtChallengeResult) => {
        this.loading = false;
        if (res.status === 'CRISIS_DETECTED' && res.data) {
          this.crisisService.triggerCrisisAlert(
            res.data.message || 'Identificamos sofrimento agudo. Por favor, acesse os canais de apoio imediato.',
            res.data.helplines || []
          );
          this.structuredResult = null;
        } else {
          this.structuredResult = res.data || res;
        }
      },
      error: (err) => {
        this.loading = false;
        console.error(err);
      }
    });
  }

  getDistortionsList(): string[] {
    if (!this.structuredResult) return [];
    if (Array.isArray(this.structuredResult.detected_distortions)) {
      return this.structuredResult.detected_distortions;
    }
    if (typeof this.structuredResult.distortions === 'string') {
      return this.structuredResult.distortions.split(',').map((s: string) => s.trim());
    }
    return [];
  }
}
