import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'yellow' | 'coral' | 'green' | 'blue' | 'gray';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'yellow',
  className = '',
}) => {
  const colorMap = {
    yellow: 'bg-electric-yellow text-black',
    coral: 'bg-coral-500 text-white',
    green: 'bg-fresh-green text-black',
    blue: 'bg-cobalt-500 text-white',
    gray: 'bg-cream-200 text-ink',
  };

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 text-xs font-black border border-black uppercase tracking-wider ${colorMap[variant]} ${className}`}
    >
      {children}
    </span>
  );
};
