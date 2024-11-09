import React from 'react';

const CustomAlert = ({ variant = 'default', children, className = '' }) => {
  const baseStyles = "p-4 rounded-lg mb-4 flex items-start gap-2";
  const variantStyles = {
    default: "bg-blue-500/10 text-blue-200 border border-blue-500/20",
    destructive: "bg-red-900/50 border-red-500 text-red-200 border",
    warning: "bg-yellow-500/10 text-yellow-200 border border-yellow-500/20",
    success: "bg-green-500/10 text-green-200 border border-green-500/20"
  };

  return (
    <div className={`${baseStyles} ${variantStyles[variant]} ${className}`}>
      {children}
    </div>
  );
};

export { CustomAlert };