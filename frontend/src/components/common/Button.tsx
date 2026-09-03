import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'coral' | 'white' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className = '',
  disabled,
  ...props
}) => {
  let variantClass = 'btn-brutal';
  if (variant === 'coral') variantClass = 'btn-brutal-coral';
  else if (variant === 'white') variantClass = 'btn-brutal-white';
  else if (variant === 'ghost') variantClass = 'font-bold px-3 py-1.5 hover:underline text-ink';

  const sizeClass = size === 'sm' ? 'text-xs py-1 px-3' : size === 'lg' ? 'text-lg py-3.5 px-8' : 'text-sm py-2 px-4';

  return (
    <button
      disabled={disabled || isLoading}
      className={`${variantClass} ${sizeClass} ${className}`}
      {...props}
    >
      {isLoading ? 'Loading...' : children}
    </button>
  );
};
