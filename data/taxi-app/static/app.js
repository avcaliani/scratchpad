const FLAG_KEYS = [
  'flag_invalid_fare',
  'flag_invalid_distance',
  'flag_invalid_timestamp',
  'flag_unrealistic_distance',
  'flag_unrealistic_fare',
  'flag_zero_distance_paid',
];

function app() {
  return {
    tripId: '',
    loading: false,
    result: null,
    error: null,

    async search() {
      this.result = null;
      this.error = null;
      this.loading = true;
      try {
        const res = await fetch(`/api/trips/${this.tripId}`);
        if (res.ok) {
          this.result = await res.json();
        } else if (res.status === 404) {
          this.error = '🔍 Trip not found.';
        } else if (res.status === 400) {
          this.error = '⚠️ Invalid trip ID format.';
        } else if (res.status === 503) {
          this.error = '🔧 Service unavailable. Try again shortly.';
        } else {
          this.error = '💥 An unexpected error occurred.';
        }
      } catch {
        this.error = '📡 Could not reach the API.';
      } finally {
        this.loading = false;
      }
    },

    fmtDate(val) {
      if (val == null) return '—';
      return new Date(val).toLocaleString();
    },

    qualityFlags() {
      if (!this.result) return [];
      return FLAG_KEYS.map(k => [k, this.result[k]]);
    },
  };
}
