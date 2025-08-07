import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from '../../pages/Dashboard';

// Mock framer-motion to avoid animation issues in tests
jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
    nav: ({ children, ...props }: any) => <nav {...props}>{children}</nav>,
    h1: ({ children, ...props }: any) => <h1 {...props}>{children}</h1>,
    h2: ({ children, ...props }: any) => <h2 {...props}>{children}</h2>,
    h3: ({ children, ...props }: any) => <h3 {...props}>{children}</h3>,
    p: ({ children, ...props }: any) => <p {...props}>{children}</p>,
    span: ({ children, ...props }: any) => <span {...props}>{children}</span>,
    a: ({ children, ...props }: any) => <a {...props}>{children}</a>,
  },
  useScroll: () => ({ scrollY: { onChange: jest.fn(), get: () => 0 } }),
  useTransform: () => 'rgba(0, 0, 0, 0)',
}));

// Mock the CreditScoreCalculator component
jest.mock('../../components/CreditScoreCalculator', () => {
  return function MockCreditScoreCalculator({ targetScore }: { targetScore: number }) {
    return <div data-testid="credit-score-calculator">Score: {targetScore}</div>;
  };
});

// Mock the Navigation component
jest.mock('../../components/Navigation', () => {
  return function MockNavigation() {
    return <nav data-testid="navigation">Navigation</nav>;
  };
});

// Mock the OrbBackground component
jest.mock('../../components/ui/OrbBackground', () => {
  return function MockOrbBackground() {
    return <div data-testid="orb-background">Background</div>;
  };
});

const renderDashboard = () => {
  return render(
    <BrowserRouter>
      <Dashboard />
    </BrowserRouter>
  );
};

describe('Dashboard', () => {
  test('renders dashboard title', () => {
    renderDashboard();
    expect(screen.getByText('Your Credit Dashboard')).toBeInTheDocument();
  });

  test('renders credit score section', () => {
    renderDashboard();
    expect(screen.getByText('Latest Credit Score')).toBeInTheDocument();
    expect(screen.getByTestId('credit-score-calculator')).toBeInTheDocument();
  });

  test('renders score trend section', () => {
    renderDashboard();
    expect(screen.getByText('📈 Score Trend')).toBeInTheDocument();
  });

  test('renders personalized insights section', () => {
    renderDashboard();
    expect(screen.getByText('💡 Personalized Insights')).toBeInTheDocument();
  });

  test('renders profile completeness section', () => {
    renderDashboard();
    expect(screen.getByText('📊 Profile Completeness')).toBeInTheDocument();
  });

  test('renders badges section', () => {
    renderDashboard();
    expect(screen.getByText('🏅 Your Badges')).toBeInTheDocument();
  });

  test('renders recent activity section', () => {
    renderDashboard();
    expect(screen.getByText('🕒 Recent Activity')).toBeInTheDocument();
  });

  test('renders download report button', () => {
    renderDashboard();
    expect(screen.getByText('Download Report')).toBeInTheDocument();
  });

  test('displays mock credit score', () => {
    renderDashboard();
    expect(screen.getByText('Score: 712')).toBeInTheDocument();
  });

  test('displays score factors', () => {
    renderDashboard();
    expect(screen.getByText('Rent Payment Consistency')).toBeInTheDocument();
    expect(screen.getByText('Utility Payment History')).toBeInTheDocument();
  });

  test('displays badges', () => {
    renderDashboard();
    expect(screen.getByText('Rent Rockstar')).toBeInTheDocument();
    expect(screen.getByText('Utility Champion')).toBeInTheDocument();
    expect(screen.getByText('Score Climber')).toBeInTheDocument();
  });

  test('displays insights', () => {
    renderDashboard();
    expect(screen.getByText('Score Improvement')).toBeInTheDocument();
    expect(screen.getByText('Boost Your Score')).toBeInTheDocument();
    expect(screen.getByText('Missing Data')).toBeInTheDocument();
  });
});
