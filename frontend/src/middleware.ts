import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Define allowed routes
const PUBLIC_ROUTES = ["/login"];
const PROTECTED_ROUTES = [
  "/dashboard",
  "/accounts",
  "/admin",
  "/feedback",
  "/stocks",
  "/settings",
];

// Admin-only routes
const ADMIN_ROUTES = ["/admin"];

export function middleware(req: NextRequest) {
  const token = req.cookies.get("token")?.value;
  const pathname = req.nextUrl.pathname;

  // Check if route is public
  const isPublicRoute = PUBLIC_ROUTES.some((route) => pathname.startsWith(route));

  // Check if route is protected
  const isProtectedRoute = PROTECTED_ROUTES.some((route) => pathname.startsWith(route));

  // Check if route requires admin
  const isAdminRoute = ADMIN_ROUTES.some((route) => pathname.startsWith(route));

  // 1️⃣ If NOT logged in and trying to access protected route → redirect to /login
  if (!token && isProtectedRoute) {
    const loginUrl = new URL("/login", req.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // 2️⃣ If logged in and tries to access login → redirect to /dashboard
  if (token && isPublicRoute) {
    return NextResponse.redirect(new URL("/dashboard", req.url));
  }

  // 3️⃣ If accessing non-existent routes (not public, not protected, not static) → redirect to dashboard
  if (!isPublicRoute && !isProtectedRoute && !pathname.startsWith("/_next") && !pathname.startsWith("/api")) {
    if (token) {
      return NextResponse.redirect(new URL("/dashboard", req.url));
    } else {
      return NextResponse.redirect(new URL("/login", req.url));
    }
  }

  // 4️⃣ For admin routes, we'll verify in the page component (since we can't access localStorage in middleware)
  // The middleware just ensures they're authenticated

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!_next|favicon.ico|api|static|images|fonts).*)",
  ],
};

