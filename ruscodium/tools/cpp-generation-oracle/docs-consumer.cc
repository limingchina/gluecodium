#include "oracle/docs/Data.h"
#include "oracle/docs/Service.h"
#include "oracle/docs/OnlyJava.h"
#include <cassert>
#include <string>

class Service final : public oracle::docs::Service {
public:
    int32_t transform(int32_t value) override { return value + 1; }
    void hidden() override {}
    int32_t get_value() const override { return value_; }
    void set_value(int32_t value) override { value_ = value; }
private:
    int32_t value_ = 0;
};

int main() {
    oracle::docs::Data data("text", 7);
    Service service;
    service.set_value(data.count);
    assert(service.transform(service.get_value()) == 8);
    assert(data.label == "text");
    oracle::docs::OnlyJava value = 3;
    assert(value == 3);
}
