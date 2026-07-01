import axios from 'axios';

// ==================== INTERFACES ====================

export interface UserCreate {
  email: string;
  password: string;
  name: string;
}

export interface UserResponse {
  id: number;
  email: string;
  name: string;
  accountStatus: string;
  isAuthenticated: boolean;
}

export interface UserUpdate {
  email?: string;
  password?: string;
  name?: string;
}

export interface RegistrationRequest {
  email: string;
  password: string;
  name: string;
}

export interface RegistrationResponse {
  userId: number;
  email: string;
  message: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  userId: number;
  email: string;
  name: string;
  message: string;
}

export interface PostCreateDTO {
  authorId: string;
  textContent: string;
}

export interface PostResponseDTO {
  id: number;
  authorId: string;
  textContent: string;
}

export interface PostUpdateDTO {
  textContent?: string;
}

export interface CommentCreate {
  content: string;
}

export interface CommentResponse {
  id: number;
  content: string;
}

export interface CommentUpdate {
  content?: string;
}

export interface FollowRequest {
  initiatorId: string;
  targetProfileId: string;
}

export interface UnfollowRequest {
  initiatorId: string;
  targetProfileId: string;
}

export interface FollowResponse {
  success: boolean;
  newFollowerCount: number;
  message: string;
}

export interface FriendshipCreate {
  abstract_isMutual: boolean;
}

export interface FriendshipResponse {
  id: number;
  abstract_isMutual: boolean;
}

export interface FriendRequestCreate {
  pending: boolean;
  abstract_isDuplicate: boolean;
  notification_id: number;
}

export interface FriendRequestResponse {
  id: number;
  pending: boolean;
  abstract_isDuplicate: boolean;
  notification_id?: number;
}

export interface GroupCreate {
  groupName_id: number;
  groupResource_id: number;
}

export interface GroupResponse {
  id: number;
  groupName_id?: number;
  groupResource_id?: number;
}

export interface GroupMembershipCreate {
  groupId: string;
  userId: string;
  group_id: number;
}

export interface GroupMembershipResponse {
  userId: string;
  groupId: string;
  group_id?: number;
}

export interface JoinRequestCreate {
  requestId: string;
  userId: string;
  groupId: string;
  group_id: number;
}

export interface JoinRequestResponse {
  userId: string;
  requestId: string;
  groupId: string;
  group_id?: number;
}

export interface NotificationCreate {
  like_id: number;
  comment_id: number;
}

export interface NotificationResponse {
  id: number;
  like_id?: number;
  comment_id?: number;
}

export interface NotificationPreferenceCreate {
  userId: string;
  enabled: boolean;
}

export interface NotificationPreferenceResponse {
  userId: string;
  enabled: boolean;
}

export interface BookmarkCreate {
  userId: string;
  postId: string;
}

export interface BookmarkResponse {
  userId: string;
  postId: string;
}

export interface SavedListCreate {
  userId: string;
}

export interface SavedListResponse {
  userId: string;
}

export interface UserProfileCreate {
  verifiedBadgeStatus: boolean;
}

export interface UserProfileResponse {
  id: number;
  verifiedBadgeStatus: boolean;
}

export interface AuditLogCreate {
  adminId: string;
  actionType: string;
  targetUserId: string;
}

export interface AuditLogResponse {
  id: number;
  adminId: string;
  actionType: string;
  targetUserId: string;
}

export interface LikeResponse {
  id: number;
}

export interface MessageResponse {
  id: number;
}

export interface ReportResponse {
  id: number;
}

export interface BlockResponse {
  id: number;
}

export interface ProfileResponse {
  id: number;
}

export interface PhotoResponse {
  id: number;
  profile_id?: number;
}

export interface BiographyResponse {
  id: number;
  profile_id?: number;
}

export interface RoleResponse {
  id: number;
  name: string;
}

export interface ActorResponse {
  id: string;
  name: string;
}

export interface VerifiedBadgeResponse {
  id: number;
}

// ==================== SERVICE ====================

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ==================== AUTH / USER ====================

export async function registerUser(data: RegistrationRequest): Promise<RegistrationResponse> {
  const res = await api.post('/users/register', data);
  return res.data;
}

export async function loginUser(data: LoginRequest): Promise<LoginResponse> {
  const res = await api.post('/users/login', data);
  return res.data;
}

export async function listUsers(): Promise<UserResponse[]> {
  const res = await api.get('/users/');
  return res.data;
}

export async function getUser(userId: number): Promise<UserResponse> {
  const res = await api.get(`/users/${userId}`);
  return res.data;
}

export async function updateUser(userId: number, data: UserUpdate): Promise<UserResponse> {
  const res = await api.put(`/users/${userId}`, data);
  return res.data;
}

export async function deleteUser(userId: number): Promise<void> {
  await api.delete(`/users/${userId}`);
}

// ==================== POSTS ====================

export async function listPosts(): Promise<PostResponseDTO[]> {
  const res = await api.get('/posts');
  return res.data;
}

export async function getPost(postId: number): Promise<PostResponseDTO> {
  const res = await api.get(`/posts/${postId}`);
  return res.data;
}

export async function createPost(data: PostCreateDTO): Promise<PostResponseDTO> {
  const res = await api.post('/posts', data);
  return res.data;
}

export async function updatePost(postId: number, data: PostUpdateDTO): Promise<PostResponseDTO> {
  const res = await api.put(`/posts/${postId}`, data);
  return res.data;
}

export async function deletePost(postId: number): Promise<void> {
  await api.delete(`/posts/${postId}`);
}

// ==================== COMMENTS ====================

export async function listComments(): Promise<CommentResponse[]> {
  const res = await api.get('/comments');
  return res.data;
}

export async function getComment(commentId: number): Promise<CommentResponse> {
  const res = await api.get(`/comments/${commentId}`);
  return res.data;
}

export async function createComment(data: CommentCreate): Promise<CommentResponse> {
  const res = await api.post('/comments', data);
  return res.data;
}

export async function updateComment(commentId: number, data: CommentUpdate): Promise<CommentResponse> {
  const res = await api.put(`/comments/${commentId}`, data);
  return res.data;
}

export async function deleteComment(commentId: number): Promise<void> {
  await api.delete(`/comments/${commentId}`);
}

// ==================== LIKES ====================

export async function listLikes(): Promise<any[]> {
  const res = await api.get('/likes');
  return res.data;
}

export async function createLike(): Promise<any> {
  const res = await api.post('/likes', {});
  return res.data;
}

export async function deleteLike(likeId: number): Promise<void> {
  await api.delete(`/likes/${likeId}`);
}

// ==================== FOLLOWS ====================

export async function followUser(data: FollowRequest): Promise<FollowResponse> {
  const res = await api.post('/follow', data);
  return res.data;
}

export async function unfollowUser(data: UnfollowRequest): Promise<FollowResponse> {
  const res = await api.post('/unfollow', data);
  return res.data;
}

// ==================== FRIENDSHIPS ====================

export async function listFriendships(): Promise<FriendshipResponse[]> {
  const res = await api.get('/friendships');
  return res.data;
}

export async function createFriendship(data: FriendshipCreate): Promise<FriendshipResponse> {
  const res = await api.post('/friendships', data);
  return res.data;
}

// ==================== FRIEND REQUESTS ====================

export async function listFriendRequests(): Promise<FriendRequestResponse[]> {
  const res = await api.get('/friend_requests');
  return res.data;
}

export async function createFriendRequest(data: FriendRequestCreate): Promise<FriendRequestResponse> {
  const res = await api.post('/friend_requests', data);
  return res.data;
}

// ==================== GROUPS ====================

export async function listGroups(): Promise<GroupResponse[]> {
  const res = await api.get('/groups');
  return res.data;
}

export async function createGroup(data: GroupCreate): Promise<GroupResponse> {
  const res = await api.post('/groups', data);
  return res.data;
}

// ==================== GROUP MEMBERSHIPS ====================

export async function listGroupMemberships(): Promise<GroupMembershipResponse[]> {
  const res = await api.get('/group_memberships');
  return res.data;
}

export async function createGroupMembership(data: GroupMembershipCreate): Promise<GroupMembershipResponse> {
  const res = await api.post('/group_memberships', data);
  return res.data;
}

// ==================== JOIN REQUESTS ====================

export async function listJoinRequests(): Promise<JoinRequestResponse[]> {
  const res = await api.get('/join_requests');
  return res.data;
}

export async function createJoinRequest(data: JoinRequestCreate): Promise<JoinRequestResponse> {
  const res = await api.post('/join_requests', data);
  return res.data;
}

// ==================== NOTIFICATIONS ====================

export async function listNotifications(): Promise<NotificationResponse[]> {
  const res = await api.get('/notifications');
  return res.data;
}

export async function createNotification(data: NotificationCreate): Promise<NotificationResponse> {
  const res = await api.post('/notifications', data);
  return res.data;
}

// ==================== NOTIFICATION PREFERENCES ====================

export async function listNotificationPreferences(): Promise<NotificationPreferenceResponse[]> {
  const res = await api.get('/notification_preferences');
  return res.data;
}

export async function createNotificationPreference(data: NotificationPreferenceCreate): Promise<NotificationPreferenceResponse> {
  const res = await api.post('/notification_preferences', data);
  return res.data;
}

// ==================== BOOKMARKS ====================

export async function listBookmarks(): Promise<BookmarkResponse[]> {
  const res = await api.get('/bookmarks');
  return res.data;
}

export async function createBookmark(data: BookmarkCreate): Promise<BookmarkResponse> {
  const res = await api.post('/bookmarks', data);
  return res.data;
}

// ==================== SAVED LISTS ====================

export async function listSavedLists(): Promise<SavedListResponse[]> {
  const res = await api.get('/saved_lists');
  return res.data;
}

export async function createSavedList(data: SavedListCreate): Promise<SavedListResponse> {
  const res = await api.post('/saved_lists', data);
  return res.data;
}

// ==================== USER PROFILES ====================

export async function listUserProfiles(): Promise<UserProfileResponse[]> {
  const res = await api.get('/user_profiles');
  return res.data;
}

export async function getUserProfile(profileId: number): Promise<UserProfileResponse> {
  const res = await api.get(`/user_profiles/${profileId}`);
  return res.data;
}

export async function updateUserProfile(profileId: number, data: UserProfileCreate): Promise<UserProfileResponse> {
  const res = await api.put(`/user_profiles/${profileId}`, data);
  return res.data;
}

// ==================== AUDIT LOGS ====================

export async function listAuditLogs(): Promise<AuditLogResponse[]> {
  const res = await api.get('/audit_logs');
  return res.data;
}

export async function createAuditLog(data: AuditLogCreate): Promise<AuditLogResponse> {
  const res = await api.post('/audit_logs', data);
  return res.data;
}
