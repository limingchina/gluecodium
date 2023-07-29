// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "ExportGluecodiumCpp.h"

namespace test {
/**
 * Test class for cross reference of enum values without under score. Always working.

 */
class _GLUECODIUM_CPP_EXPORT TestClassEnumValueWithoutUnderScore {
public:
    TestClassEnumValueWithoutUnderScore();
    virtual ~TestClassEnumValueWithoutUnderScore() = 0;


public:
    /**
     * Note:a ::test::Error::INTERNAL error is generated.
     */
    virtual void foo_good_case(  ) = 0;
    /**
     * *Note: ::test::Error::INTERNAL error is generated.
     */
    virtual void foo_star_good_case1(  ) = 0;
    /**
     * Note:* ::test::Error::INTERNAL error is generated.
     */
    virtual void foo_star_good_case2(  ) = 0;
    /**
     * This is a test
     *
     * **Note:** ::test::Error::INTERNAL is generated.
     */
    virtual void foo_sentence_with_a_new_line_good_case(  ) = 0;
    /**
     * This is a tes
     *
     * **Note:** ::test::Error::INTERNAL is generated.
     */
    virtual void foo_shorter_sentence_with_a_new_line_good_case(  ) = 0;
};


}
