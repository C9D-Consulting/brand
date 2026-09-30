// Server configuration, read lazily so a missing value fails the request that
// needs it with a clear message, rather than the whole build.

function required(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing environment variable ${name}. See .env.example.`);
  return value;
}

export const env = {
  get appUrl() {
    return (process.env.APP_URL ?? (process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : 'http://localhost:3000')).replace(/\/$/, '');
  },
  get adminPassword() {
    return required('ADMIN_PASSWORD');
  },
  get sessionSecret() {
    return required('SESSION_SECRET');
  },
  get tokenEncryptionKey() {
    return required('TOKEN_ENCRYPTION_KEY');
  },
  get googleClientId() {
    return required('GOOGLE_CLIENT_ID');
  },
  get googleClientSecret() {
    return required('GOOGLE_CLIENT_SECRET');
  },
  get supabaseUrl() {
    return required('SUPABASE_URL');
  },
  get supabaseServiceRoleKey() {
    return required('SUPABASE_SERVICE_ROLE_KEY');
  },
  get cronSecret() {
    return process.env.CRON_SECRET ?? '';
  },
};
