import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  interactive?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  interactive = false,
}) => {
  return (
    <div
      className={`${
        interactive ? 'card-brutal-interactive' : 'card-brutal'
      } bg-white p-6 ${className}`}
    >
      {children}
    </div>
  );
};
