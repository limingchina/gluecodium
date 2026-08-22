cmake_minimum_required(VERSION 3.20)
project(gluecodium_phase4_harness LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(GLUECODIUM_ROOT "${CMAKE_CURRENT_LIST_DIR}/../../.." CACHE PATH "Gluecodium repository root")
set(GLUECODIUM_GRADLE "${GLUECODIUM_ROOT}/gradlew")
set(HARNESS_INPUT "${CMAKE_CURRENT_LIST_DIR}/input")
set(GENERATED_ROOT "${CMAKE_CURRENT_BINARY_DIR}/generated")

execute_process(
    COMMAND "${GLUECODIUM_GRADLE}" :gluecodium:run
        "--args=-input \"${HARNESS_INPUT}\" -output \"${GENERATED_ROOT}\" -generators cpp,js"
    WORKING_DIRECTORY "${GLUECODIUM_ROOT}"
    RESULT_VARIABLE GENERATE_RESULT
)
if(NOT GENERATE_RESULT EQUAL 0)
    message(FATAL_ERROR "Gluecodium generation failed: ${GENERATE_RESULT}")
endif()

configure_file(
    "${CMAKE_CURRENT_LIST_DIR}/test.mjs"
    "${CMAKE_CURRENT_BINARY_DIR}/test.mjs"
    COPYONLY
)

file(GLOB GENERATED_CPP CONFIGURE_DEPENDS
    "${GENERATED_ROOT}/js/embind/*.cpp"
    "${GENERATED_ROOT}/cpp/src/*.cpp"
    "${GENERATED_ROOT}/cpp/src/**/*.cpp"
)

add_executable(phase4_harness
    harness.cpp
    ${GENERATED_CPP}
)
target_compile_options(phase4_harness PRIVATE
    "-iquote${GENERATED_ROOT}/cpp/include"
)
target_link_options(phase4_harness PRIVATE
    "-lembind"
    "-fexceptions"
    "-sMODULARIZE=1"
    "-sEXPORT_ES6=1"
    "-sWASM_BIGINT=1"
    "-sALLOW_MEMORY_GROWTH=1"
)
set_target_properties(phase4_harness PROPERTIES
    OUTPUT_NAME "phase4_harness"
    SUFFIX ".mjs"
)
