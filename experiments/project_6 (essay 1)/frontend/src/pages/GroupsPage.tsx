
import { useState, useEffect } from 'react';
import { listGroups, listGroupMemberships, listJoinRequests, createGroupMembership, createJoinRequest } from '../api/services';
import type { GroupResponse, GroupMembershipResponse, JoinRequestResponse } from '../types';

export default function GroupsPage() {
  const [groups, setGroups] = useState<GroupResponse[]>([]);
  const [memberships, setMemberships] = useState<GroupMembershipResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([listGroups(), listGroupMemberships()])
      .then(([g, m]) => {
        setGroups(g);
        setMemberships(m);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="page"><p>Loading groups...</p></div>;

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Groups</h1>
      {groups.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No groups yet</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
          {groups.map((group) => {
            const memberCount = memberships.filter((m) => m.group_id === group.id || Number(m.groupId) === group.id).length;
            return (
              <div key={group.id} className="card">
                <h3>Group #{group.id}</h3>
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem', flexWrap: 'wrap' }}>
                  <span className="badge">{memberCount} members</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
