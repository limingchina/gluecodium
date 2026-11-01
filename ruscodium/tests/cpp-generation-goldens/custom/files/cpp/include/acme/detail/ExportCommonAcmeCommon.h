// -------------------------------------------------------------------------------------------------
//
// Copyright 2026 Example
// All rights reserved.
//
// -------------------------------------------------------------------------------------------------

#pragma once

#ifdef ACME_COMMON_SHARED
#   if defined(_WIN32) || defined(__CYGWIN)
#       ifdef ACME_COMMON_INTERNAL
#           define ACME_COMMON_EXPORT __declspec( dllexport )
#       else
#           define ACME_COMMON_EXPORT __declspec( dllimport )
#       endif
#   else
#       define ACME_COMMON_EXPORT __attribute__( ( visibility( "default" ) ) )
#   endif
#else
#   define ACME_COMMON_EXPORT
#endif
