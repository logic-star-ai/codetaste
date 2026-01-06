# Refactor ConsensusV2 to use dedicated variant for single-owner

Simplify consensus object ownership representation by replacing `Owner::ConsensusV2 { authenticator: Box<Authenticator> }` with `Owner::ConsensusAddressOwner { owner: SuiAddress }` and removing the `Authenticator` type entirely.