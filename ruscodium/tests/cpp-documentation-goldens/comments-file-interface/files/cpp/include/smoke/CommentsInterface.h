// -------------------------------------------------------------------------------------------------
//

//
// -------------------------------------------------------------------------------------------------

#pragma once

#include "gluecodium/ExportGluecodiumCpp.h"
#include "gluecodium/TypeRepository.h"
#include <cstdint>
#include <string>

namespace smoke {
/**
 * This is some very useful interface.

 */
class _GLUECODIUM_CPP_EXPORT CommentsInterface {
public:
    CommentsInterface();
    virtual ~CommentsInterface();


public:
    /**
     * This is some very useful enum.

     */
    enum class SomeEnum {
        /**
         * Not quite useful

         */
        USELESS,
        /**
         * Somewhat useful

         */
        USEFUL
    };



    /**
     * This is some very useful typedef.

     */
    using Usefulness = bool;

    /**
     * This is some very useful struct.

     */
    struct _GLUECODIUM_CPP_EXPORT SomeStruct {
        /**
         * How useful this struct is

         */
        ::smoke::CommentsInterface::Usefulness some_field;

        SomeStruct( );
        explicit SomeStruct( ::smoke::CommentsInterface::Usefulness some_field );

    };

    /**
     * This is some very useful constant.

     */
    static const ::smoke::CommentsInterface::Usefulness VERY_USEFUL;

public:
    /**
     * This is some very useful method that measures the usefulness of its input.
     * \param[in] input Very useful input parameter
     * \return Usefulness of the input
     */
    virtual ::smoke::CommentsInterface::Usefulness some_method_with_all_comments( const ::std::string& input ) = 0;
    /**
     * This is some very useful method that measures the usefulness of its input.
     * \param[in] input Very useful input parameter
     * \return
     */
    virtual ::smoke::CommentsInterface::Usefulness some_method_with_input_comments( const ::std::string& input ) = 0;
    /**
     * This is some very useful method that measures the usefulness of its input.
     * \param[in] input
     * \return Usefulness of the input
     */
    virtual ::smoke::CommentsInterface::Usefulness some_method_with_output_comments( const ::std::string& input ) = 0;
    /**
     * This is some very useful method that measures the usefulness of its input.
     * \param[in] input
     * \return
     */
    virtual ::smoke::CommentsInterface::Usefulness some_method_with_no_comments( const ::std::string& input ) = 0;
    /**
     * This is some very useful method that does not measure the usefulness of its input.
     * \param[in] input Very useful input parameter
     */
    virtual void some_method_without_return_type_with_all_comments( const ::std::string& input ) = 0;
    /**
     * This is some very useful method that does not measure the usefulness of its input.
     * \param[in] input
     */
    virtual void some_method_without_return_type_with_no_comments( const ::std::string& input ) = 0;
    /**
     * This is some very useful method that measures the usefulness of something.
     * \return Usefulness of the input
     */
    virtual ::smoke::CommentsInterface::Usefulness some_method_without_input_parameters_with_all_comments(  ) = 0;
    /**
     * This is some very useful method that measures the usefulness of something.
     * \return
     */
    virtual ::smoke::CommentsInterface::Usefulness some_method_without_input_parameters_with_no_comments(  ) = 0;
    virtual void some_method_with_nothing(  ) = 0;
    /**
     * This is some very useful method that does nothing.
     */
    virtual void some_method_without_return_type_or_input_parameters(  ) = 0;
    /**
     * Gets some very useful property.
     * \return Some very useful property.
     */
    virtual ::smoke::CommentsInterface::Usefulness is_some_property(  ) const = 0;
    /**
     * Sets some very useful property.
     * \param[in] value Some very useful property.
     */
    virtual void set_some_property( const ::smoke::CommentsInterface::Usefulness value ) = 0;

};


}
