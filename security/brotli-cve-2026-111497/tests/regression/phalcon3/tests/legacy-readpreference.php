<?php
// Legacy libraries use integer modes. These must work with all diagnostics enabled.
error_reporting(E_ALL);
set_error_handler(function ($severity, $message, $file, $line) {
    throw new ErrorException($message, 0, $severity, $file, $line);
});
if (phpversion('mongodb') !== '1.19.4') exit(1);
$modes = [
    MongoDB\Driver\ReadPreference::RP_PRIMARY => 'primary',
    MongoDB\Driver\ReadPreference::RP_PRIMARY_PREFERRED => 'primaryPreferred',
    MongoDB\Driver\ReadPreference::RP_SECONDARY => 'secondary',
    MongoDB\Driver\ReadPreference::RP_SECONDARY_PREFERRED => 'secondaryPreferred',
    MongoDB\Driver\ReadPreference::RP_NEAREST => 'nearest',
];
foreach ($modes as $integer => $string) {
    $old = new MongoDB\Driver\ReadPreference($integer);
    $modern = new MongoDB\Driver\ReadPreference($string);
    if ($old->getModeString() !== $string || $old->bsonSerialize() != $modern->bsonSerialize()) exit(2);
}
echo 'legacy-readpreference-ok';
