// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "gluecodium/ExportGluecodiumCpp.h"
#include <cstdint>
#include <string>

namespace smoke {
/**
 * Cpp is included for methods that need a native implementation.

 */
class _GLUECODIUM_CPP_EXPORT OnlyFunctions {
public:
    OnlyFunctions();
    virtual ~OnlyFunctions();


public:
    static const int32_t CPP_CONSTANT;

public:
    /**
     *
     * \param[in] input String to round trip through the native implementation.
     * \return The unchanged input.
     */
    static ::std::string java_only( const ::std::string& input );
    /**
     *
     * \param[in] input String to round trip through the native implementation.
     * \return The unchanged input.
     */
    static ::std::string kotlin_only( const ::std::string& input );
    /**
     *
     * \param[in] input String to round trip through the native implementation.
     * \return The unchanged input.
     */
    static ::std::string swift_only( const ::std::string& input );
    /**
     *
     * \param[in] input String to round trip through the native implementation.
     * \return The unchanged input.
     */
    static ::std::string dart_only( const ::std::string& input );
    /**
     *
     * \param[in] input String to round trip through the native implementation.
     * \return The unchanged input.
     */
    static ::std::string cpp_only( const ::std::string& input );
    /**
     *
     * \param[in] input String to round trip through the native implementation.
     * \return The unchanged input.
     */
    static ::std::string shared( const ::std::string& input );
};


}
