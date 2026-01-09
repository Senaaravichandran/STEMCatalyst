import React from "react";
import { buttonVariants } from "../lib/utils";
import { cn } from "../lib/utils";

export const Button = React.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
  const Comp = "button";
  return (
    <Comp
      className={cn(buttonVariants({ variant, size }), "transition-all duration-200 hover:scale-105", className)}
      ref={ref}
      {...props}
    />
  );
});

Button.displayName = "Button";
