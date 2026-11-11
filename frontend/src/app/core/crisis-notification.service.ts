import { Injectable, signal } from '@angular/core';

export interface CrisisHelpline {
  name: string;
  phone: string;
  available: string;
  country: string;
}

export interface CrisisAlertState {
  isActive: boolean;
  message: string;
  helplines: CrisisHelpline[];
}

@Injectable({
  providedIn: 'root'
})
export class CrisisNotificationService {
  private state = signal<CrisisAlertState>({
    isActive: false,
    message: '',
    helplines: []
  });

  readonly crisisState = this.state.asReadonly();

  triggerCrisisAlert(message: string, helplines: CrisisHelpline[]) {
    this.state.set({
      isActive: true,
      message,
      helplines
    });
  }

  dismissAlert() {
    this.state.set({
      isActive: false,
      message: '',
      helplines: []
    });
  }
}
