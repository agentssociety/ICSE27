
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import SearchPage from '../pages/SearchPage';

vi.mock('../api/services', () => ({
  listPosts: vi.fn().mockResolvedValue([]),
  listUsers: vi.fn().mockResolvedValue([]),
}));

describe('SearchPage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<SearchPage />);
    });
    expect(screen.getByPlaceholderText('Search users and posts...')).toBeInTheDocument();
  });

  it('has search input', async () => {
    await act(async () => {
      render(<SearchPage />);
    });
    expect(screen.getByPlaceholderText('Search users and posts...')).toBeInTheDocument();
  });
});
