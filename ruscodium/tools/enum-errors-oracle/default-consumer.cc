#include "oracle/customerrors/RenamedError.h"
#include "oracle/customerrors/Worker.h"
#include <cassert>
#include <string>
#include <system_error>
using Error = oracle::customerrors::RenamedError;
class Concrete final : public oracle::customerrors::Worker {
public:
    std::error_code call(bool fail) override {
        return fail ? std::error_code(Error::BAD) : std::error_code{};
    }
    Return<int32_t, std::error_code> value(bool fail) override {
        if (fail) return std::error_code(Error::BAD);
        return int32_t{8};
    }
};
int main() {
    Concrete service;
    auto failure = service.value(true);
    auto value = service.value(false);
    assert(!service.call(false) && service.call(true) == Error::BAD);
    assert(!failure.has_value() && failure.error() == Error::BAD);
    assert(value.has_value() && value.unsafe_value() == 8);
    assert(std::string(failure.error().category().name()) == "RenamedErrorErrorCategory");
    assert(failure.error().message() == "::oracle::customerrors::RenamedError::BAD");
}
