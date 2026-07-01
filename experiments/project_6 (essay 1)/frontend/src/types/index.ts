
// User
export interface UserCreate {
  email: string;
  password: string;
  name: string;
}

export interface UserUpdate {
  email?: string;
  password?: string;
  name?: string;
}

export interface UserResponse {
  id: number;
  email: string;
  name: string;
  accountStatus: string;
  isAuthenticated: boolean;
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

// Posts
export interface PostCreateDTO {
  authorId: string;
  textContent: string;
}

export interface PostUpdateDTO {
  textContent?: string;
}

export interface PostResponseDTO {
  id: number;
  authorId: string;
  textContent: string;
}

// Comments
export interface CommentCreate {
  content: string;
}

export interface CommentUpdate {
  content?: string;
}

export interface CommentResponse {
  id: number;
  content: string;
}

// Follow
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

// Friendships
export interface FriendshipCreate {
  abstract_isMutual: boolean;
}

export interface FriendshipResponse {
  id: number;
  abstract_isMutual: boolean;
}

// Friend Requests
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

// Groups
export interface GroupCreate {
  groupName_id: number;
  groupResource_id: number;
}

export interface GroupResponse {
  id: number;
  groupName_id?: number;
  groupResource_id?: number;
}

// Group Memberships
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

// Join Requests
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

// Notifications
export interface NotificationCreate {
  like_id: number;
  comment_id: number;
}

export interface NotificationResponse {
  id: number;
  like_id?: number;
  comment_id?: number;
}

// Notification Preferences
export interface NotificationPreferenceCreate {
  userId: string;
  enabled: boolean;
}

export interface NotificationPreferenceResponse {
  userId: string;
  enabled: boolean;
}

// Bookmarks
export interface BookmarkCreate {
  userId: string;
  postId: string;
}

export interface BookmarkResponse {
  userId: string;
  postId: string;
}

// Saved Lists
export interface SavedListCreate {
  userId: string;
}

export interface SavedListResponse {
  userId: string;
}

// User Profiles (Verified Badge)
export interface UserProfileCreate {
  verifiedBadgeStatus: boolean;
}

export interface UserProfileResponse {
  id: number;
  verifiedBadgeStatus: boolean;
}

// Audit Logs
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

// Not used as types but need exports for services
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
