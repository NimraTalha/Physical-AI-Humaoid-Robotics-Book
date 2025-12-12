import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import NavbarItem from '@theme/NavbarItem';
import ClientOnly from '@docusaurus/core/lib/client/ClientOnly';

function AuthItems() {
  const { user, logout } = useAuth();

  if (user) {
    return (
      <>
        <NavbarItem label={`Welcome, ${user.username}`} />
        <div className="navbar__item" onClick={logout} style={{ cursor: 'pointer' }}>Logout</div>
      </>
    );
  }

  return (
    <>
      <NavbarItem href="/signup" label="Sign Up" />
      <NavbarItem href="/signin" label="Sign In" />
    </>
  );
}

export default function AuthNavbarItems() {
    return (
        <ClientOnly>
            <AuthItems />
        </ClientOnly>
    )
}