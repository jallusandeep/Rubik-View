"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import api from "@/lib/api";
import { isAuthenticated, isAdmin, getUserRole } from "@/lib/auth";

interface UseAuthOptions {
  requireAuth?: boolean;
  requireAdmin?: boolean;
  redirectTo?: string;
}

export function useAuth(options: UseAuthOptions = {}) {
  const { requireAuth = true, requireAdmin = false, redirectTo } = options;
  const router = useRouter();
  const pathname = usePathname();
  const [isLoading, setIsLoading] = useState(true);
  const [isValid, setIsValid] = useState(false);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const verifyAuth = async () => {
      if (requireAuth && !isAuthenticated()) {
        router.push(redirectTo || "/login");
        return;
      }

      if (requireAdmin && !isAdmin()) {
        router.push(redirectTo || "/dashboard");
        return;
      }

      // Verify token with backend
      if (requireAuth) {
        try {
          const response = await api.get("/auth/users/me");
          setUser(response.data);
          setIsValid(true);

          // If admin required, verify role from backend
          if (requireAdmin && response.data.role !== "admin" && response.data.role !== "superadmin") {
            router.push(redirectTo || "/dashboard");
            return;
          }
        } catch (error) {
          // Token invalid or expired
          console.error("Authentication verification failed:", error);
          const { logout } = await import("@/lib/auth");
          logout();
          return;
        }
      }

      setIsLoading(false);
    };

    verifyAuth();
  }, [requireAuth, requireAdmin, redirectTo, router, pathname]);

  return {
    isLoading,
    isValid,
    user,
    isAuthenticated: isAuthenticated(),
    isAdmin: isAdmin(),
    role: getUserRole(),
  };
}

