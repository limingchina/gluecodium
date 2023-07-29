// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "ExportGluecodiumCpp.h"

namespace test {
/**
 * Test class for cross references of enum values with under score. Some cases don't work.

 */
class _GLUECODIUM_CPP_EXPORT TestClassEnumValueWithUnderScore {
public:
    TestClassEnumValueWithUnderScore();
    virtual ~TestClassEnumValueWithUnderScore() = 0;


public:
    /**
     * Note:a ::test::Error::INVALID_PARAMETER error is generated.
     */
    virtual void foo_good_case(  ) = 0;
    /**
     * Note:* [Error.INVALID_PARAMETER] error is generated.
     */
    virtual void foo_star_bad_case1(  ) = 0;
    /**
     * *Note: [Error.INVALID_PARAMETER] error is generated.
     */
    virtual void foo_star_bad_case2(  ) = 0;
    /**
     * This is a test
     *
     * *Note: ::test::Error::INVALID_PARAMETER is generated.
     */
    virtual void foo_sentence_with_a_new_line_good_case(  ) = 0;
    /**
     * This is a tes
     *
     * *Note: [Error.INVALID_PARAMETER] is generated.
     */
    virtual void foo_shorter_sentence_with_a_new_line_bad_case(  ) = 0;
};


}
