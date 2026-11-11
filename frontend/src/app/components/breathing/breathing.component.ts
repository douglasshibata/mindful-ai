import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-breathing',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="flex flex-col items-center justify-center p-8 bg-teal-50 rounded-2xl shadow-inner mt-12">
      <h2 class="text-2xl font-semibold text-teal-800 mb-8">Take a Moment to Breathe</h2>

      <div class="relative flex items-center justify-center w-64 h-64">
        <!-- Breathing Circle -->
        <div [class]="'absolute rounded-full bg-teal-400 opacity-60 transition-all duration-[4000ms] ease-in-out ' +
                    (phase === 'Inhale' ? 'scale-100' : 'scale-50')">
        </div>
        <div class="z-10 text-2xl font-bold text-teal-900">{{phase}}</div>
      </div>

      <div class="mt-8 text-teal-700 font-medium">
        {{timer}}s remaining
      </div>

      <button (click)="toggleBreathing()" class="mt-6 px-8 py-2 bg-teal-600 text-white rounded-full hover:bg-teal-700 transition shadow-lg">
        {{active ? 'Stop' : 'Start'}} Exercise
      </button>
    </div>
  `,
  styles: [`
    .scale-100 { transform: scale(1); }
    .scale-50 { transform: scale(0.5); }
  `]
})
export class BreathingComponent implements OnInit, OnDestroy {
  phase: 'Inhale' | 'Exhale' = 'Inhale';
  timer: number = 4;
  active: boolean = false;
  private intervalId: any;

  ngOnInit() {}

  ngOnDestroy() {
    this.stop();
  }

  toggleBreathing() {
    if (this.active) this.stop();
    else this.start();
  }

  private start() {
    this.active = true;
    this.timer = 4;
    this.phase = 'Inhale';
    this.intervalId = setInterval(() => {
      this.timer--;
      if (this.timer === 0) {
        this.phase = this.phase === 'Inhale' ? 'Exhale' : 'Inhale';
        this.timer = 4;
      }
    }, 1000);
  }

  private stop() {
    this.active = false;
    if (this.intervalId) clearInterval(this.intervalId);
  }
}
