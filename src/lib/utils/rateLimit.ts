export class RateLimiter {
  private attempts: Map<string, { count: number; timestamp: number }>;
  private maxAttempts: number;
  private cooldownPeriod: number;

  constructor(maxAttempts = 3, cooldownPeriod = 60000) { // 1 minute cooldown
    this.attempts = new Map();
    this.maxAttempts = maxAttempts;
    this.cooldownPeriod = cooldownPeriod;
  }

  canAttempt(key: string): boolean {
    const now = Date.now();
    const attempt = this.attempts.get(key);

    if (!attempt) {
      this.attempts.set(key, { count: 1, timestamp: now });
      return true;
    }

    if (now - attempt.timestamp > this.cooldownPeriod) {
      this.attempts.set(key, { count: 1, timestamp: now });
      return true;
    }

    if (attempt.count >= this.maxAttempts) {
      const timeLeft = Math.ceil((this.cooldownPeriod - (now - attempt.timestamp)) / 1000);
      throw new Error(`Too many attempts. Please wait ${timeLeft} seconds.`);
    }

    attempt.count++;
    return true;
  }

  reset(key: string): void {
    this.attempts.delete(key);
  }
}