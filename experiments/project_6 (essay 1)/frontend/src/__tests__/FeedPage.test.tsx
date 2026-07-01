
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import FeedPage from '../pages/FeedPage';

vi.mock('../api/services', () => ({
  listPosts: vi.fn().mockResolvedValue([]),
  listUsers: vi.fn().mockResolvedValue([]),
  createLike: vi.fn(),
  deleteLike: vi.fn(),
}));

describe('FeedPage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<FeedPage />);
    });
    expect(screen.getByText('News Feed')).toBeInTheDocument();
  });

  it('shows empty state when no posts', async () => {
    await act(async () => {
      render(<FeedPage />);
    });
    expect(screen.getByText(/No posts yet/i)).toBeInTheDocument();
  });
});
