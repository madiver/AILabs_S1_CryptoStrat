import type { ConnectionState } from '../services/contracts';

export interface ConnectionStatusProps {
  connection: ConnectionState;
}

const labels = {
  fresh: 'Healthy',
  stale: 'Stale',
  reconnecting: 'Reconnecting',
  offline: 'Offline',
};

export function ConnectionStatus({ connection }: ConnectionStatusProps) {
  return (
    <section className={`connection-status ${connection.status}`} aria-label="Connection status">
      <strong>{labels[connection.status]}</strong>
      <span>{connection.reason ?? 'Market data connection state'}</span>
    </section>
  );
}
