import { createRoot } from 'react-dom/client';
import { App } from './App';
import './styles/base.css';
import './styles/dashboard.css';
import './styles/chart.css';

const root = document.getElementById('root');

if (!root) {
  throw new Error('Root element not found');
}

createRoot(root).render(<App />);
