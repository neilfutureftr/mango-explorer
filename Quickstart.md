# 🥭 Mango Explorer

# 🏃‍ Quickstart

Let’s assume you have a server set up already, with [docker](https://www.docker.com/) installed. This Quickstart will guide you through setting up and running [mango-explorer](https://gitlab.com/OpinionatedGeek/mango-explorer) to run a liquidator on [Mango Markets](https://mango.markets/). (You’ll need to provide your own funds for the liquidator though!)

Throughout this guide you’ll see the private key, accounts and transaction IDs as well as the commands and parameters that are used. (Funds will be removed from this account before this is published. Remember - sharing your private key is usually a Very Bad Idea!)


## 0.1 ☠️ Risks

OK, now is the time to question if you should really do this. No-one here is going to take any responsibility for your actions. It’s all on you. Are you certain you want to do this? Are you sure you want to run this code? Have you even checked it to make sure it’s not going to steal your money? Are you aware of the risks from markets in general, plus bugs, developer incompetence, malfeasance and lots of other bad stuff?


## 0.2 🦺 Prerequisites

To run this quickstart you’ll need:
* A server set up with [docker](https://www.docker.com/) or [podman](https://podman.io/) installed and configured.
* Some SOL for transaction costs.
* Some Solana-based USDT (we'll convert USDT to other tokens in this Quickstart).


# 1. ❓ Why Run A Liquidator?

Liquidation is the process that provides security to [Mango Markets](https://mango.markets/). Any accounts that borrow funds create the risk that they may not be able to pay those borrowed funds back. Accounts must provide collateral before they borrow funds, but the value of that collateral can vary with the price of the collateral tokens and the borrowed tokens.

If the value of the borrowed funds were to exceed the value of the provided collateral, all [Mango Markets](https://mango.markets/) users would have to cover those losses.

To prevent this, accounts have to provide collateral worth more than they borrow. Values are allowed to vary a little, but if the value of the collateral falls to lower than a specified threshold of what the account borrowed, that account can be 'liquidated'. (Current values for these thresholds are: you must provide collateral worth over 120% of your borrowings, and if the value of your collateral falls below 110% you can be liquidated.)

Being 'liquidated' means someone - anyone - can 'pay off' some of the borrowed tokens, in return for some of the collateral tokens. This 'paying off' earns the liquidator a premium of 5% - that is, 5% more collateral tokens are returned than the value of the borrowed tokens, making it a worthwhile task for the liquidator.

For more details of the process and what it involves, see the [Liquidation notebook](Liquidation.ipynb).


# 2. 💵 How Much Money?

This Quickstart will use 1,000USDT as the starting point. Is this enough? Too much? It all depends on you, how much you have, and how much you want to allocate to the liquidator.

1,000USDT seemed a nice starting point for this guide, but how much you use is up to you. Adjust the figures below where necessary.


# 3. 📂 Directories And Files

Our server will keep all its files under `/var/mango-explorer`, so run the following commands to set up the necessary directories and files:

```
# mkdir /var/mango-explorer
# touch /var/mango-explorer/id.json
# chown 1000:1000 /var/mango-explorer/id.json
```
(Don’t type the # prompt - that’s to show you the unix prompt where the command starts.)


# 4. 📜 'mango-explorer' Alias

Next, we'll set up an `alias` to make running the container easier. There are a lot of parameters to the
`docker` command and they're the same every time so to save typing them over and over, run:
```
# alias mango-explorer="docker run --rm -it --name=mango-explorer \
    -v /var/mango-explorer/id.json:/home/jovyan/work/id.json \
    opinionatedgeek/mango-explorer:latest"
```
_Alternatively_ if you're using `podman` instead of `docker`, run this:
```
# alias mango-explorer="podman run --rm -it --name=mango-explorer --security-opt label=disable \
    -v /var/mango-explorer/id.json:/home/jovyan/work/id.json \
    opinionatedgeek/mango-explorer:latest"
```


# 5. 👛 Create The Wallet

**Note: `solana-py` [generates 32-byte secret keys but can use 64-byte secret keys](https://github.com/michaelhly/solana-py/issues/47). This can cause problems with other software - some wallets won't accept 32-byte private keys and instead require 64-byte ones. If you want to be able to use a wallet with this account, it is recommended you create the account yourself (using your wallet?) and place the 64-byte private key in the id.json manually.**

Run the following command to create your wallet:
```
# mango-explorer create-wallet --overwrite
```
This will output a lot of text, like:
```
2021-05-08 14:14:22,984 WARNING  root         Failed to load default wallet from file 'id.json' - exception: Expecting value: line 1 column 1 (char 0)
2021-05-08 14:14:22,991 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation

Wallet for address 48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB created in file: 'id.json'.
```
That's fine - that's what a successful run of the command looks like.

This will create a Solana wallet and write its secret key to /var/mango-explorer/id.json. **Looking after this file is entirely your responsibility. If you lose this file, you lose the private key for all the funds in the wallet. If you give it to someone else you give them the entire contents of your wallet.**

Once successfully created, if you look at the file you’ll see the bytes of your private key. **Keep this secret!**

It should look something like this, but with different numbers:
```
# cat /var/mango-explorer/id.json
[248, 239, 243, 124, 6, 15, 150, 183, 123, 142, 242, 28, 140, 246, 204, 228, 202, 128, 241, 28, 133, 222, 28, 210, 131, 115, 94, 142, 22, 93, 253, 221]
```
Yes, that's the actual secret key of the account used to run the examples for this quickstart.

# 6. 💰 Add Some SOL

Transfer some SOL into the account just created. SOL tokens are needed for running operations on the Solana blockchain, similar to the way ether is used on Ethereum.

How you transfer the SOL is up to you, and dependent on where you actually have SOL.

I used [sollet](https://sollet.io) to transfer 1 SOL to **48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB**, the address shown above when creating the wallet. When the transfer completes (it’s very fast!) it appears in the wallet and you can check that using the `group-balances` command:
```
# mango-explorer group-balances
2021-05-08 14:15:51,675 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation

Balances:
    SOL balance:         1.00000000
    BTC balance:         0.00000000
    ETH balance:         0.00000000
   USDT balance:         0.00000000
```

This shows 1 SOL and 0 BTC, 0 ETH, and 0 USDT, as you'd expect (since we haven't sent any of those yet).

These three tokens - BTC, ETH, USDT - are the three tokens of the default 'group' of cross-margined tokens we're using. If you want to use a different group, you can pass the `--group-name` parameter to commands.


# 7. ✅ Validate Account

Now let's examine our account with the `Account Scout`. This tool is used to verify things on liquidator startup, and it's useful to run from time to time.

If you run it without parameters it will check the current wallet address, but you can check a different address by passing the `--address` parameter.
```
# mango-explorer account-scout
2021-05-08 14:07:30,481 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation

« ScoutReport [48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB]:
    Summary:
        Found 3 error(s) and 2 warning(s).

    Errors:
        Account '48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB' has no account for token 'BTC', mint '9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E'.
        Account '48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB' has no account for token 'ETH', mint '2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk'.
        Account '48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB' has no account for token 'USDT', mint 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB'.

    Warnings:
        No Serum open orders account for market 'BTC/USDT' [C1EuT9VokAKLiW7i2ASnZUvxDoKuKkCpDDeNxAptuNe4]'.
        No Serum open orders account for market 'ETH/USDT' [7dLVkUfBVfCGkFhSXDCq1ukM9usathSgS716t643iFGF]'.

    Details:
        Account '48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB' has no Mango Markets margin accounts.
»
```
So, we have 3 errors - no token accounts for BTC, ETH or USDT. That's expected - we haven't added any of those tokens yet. Let's start that now.


# 8. 💸 Add USDT

Transfer some USDT to the new account. Again I'm using [sollet](https://sollet.io) for this but you use whatever you're comfortable with. I transferred 1,000 USDT to **48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB**.

When you've transferred the USDT, a re-run of the `group-balances` should show something like:
```
# mango-explorer group-balances
2021-05-08 14:18:21,544 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation

Balances:
    SOL balance:         1.00000000
    BTC balance:         0.00000000
    ETH balance:         0.00000000
   USDT balance:     1,000.00000000
```

You can see above that the USDT balance is now 1,000. You should see whatever amount you transferred in your own output.


# 9. ⚖️ 'Balancing' The Wallet

The default group is a cross-margined basket of 3 tokens: BTC, ETH, and USDT. A general liquidator probably wants to be able to provide any of those tokens, to allow for situations where it needs to provide tokens to make up a margin account's shortfall.

After performing a liquidation though, the wallet may 'run out' of one type of token, or may have too much of another token, skewing the risk profile of the wallet. To fix this, we need to 'balance' the proportion of each token in the wallet.

What proportion of tokens is 'right'? It depends on your goals. You might want to accumulate only USDT, so you would specify a fixed amount of BTC and ETH as the target for balancing. On the other hand, you may just want to keep a third of the value in each token.

For our purposes here, let's go for a third in each token.

To set this up, we can use the `group-balance-wallet` command. We tell it we want to put 33% in BTC (using the `--target` parameter with the value "BTC:33%") and 33% in ETH (using the `--target` parameter with the value "ETH:33%"). Since this command actually performs transactions, let's run it first with the `--dry-run` parameter - this tells the command to run but not send any actual transactions to Serum.
```
# mango-explorer group-balance-wallet --target "BTC:33%" --target "ETH:33%" --dry-run
2021-05-08 14:20:04,522 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation

Skipping BUY trade of 0.00561444 of 'BTC'.
Skipping BUY trade of 0.09036219 of 'ETH'.
```
33% of 1,000USDT is 330 USDT, and you can see that 330 USDT is worth about 0.00561444 BTC and 0.09036219 ETH at today's prices.

Let's run it again without the `--dry-run` flag, so that it actually performs the transactions. This will place orders on the Serum orderbook to trade the tokens.
```
# mango-explorer group-balance-wallet --target "BTC:33%" --target "ETH:33%"
2021-05-08 14:28:12,940 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation

BUY order market: C1EuT9VokAKLiW7i2ASnZUvxDoKuKkCpDDeNxAptuNe4 <pyserum.market.market.Market object at 0x7f237d0894c0>
Price 61719.00 - adjusted by 0.05 from 58780
Source token account: « AccountInfo [2HchGy6FnjC6DuZb9oTZ9ByUMtUScJkhdDzGUkVNtc8T]:
    Owner: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
    Executable: False
    Lamports: 2039280
    Rent Epoch: 179                                                                                             »
Placing order                                                                                                                         paying_token_address: 2HchGy6FnjC6DuZb9oTZ9ByUMtUScJkhdDzGUkVNtc8T
    account: <solana.account.Account object at 0x7f237d147790>
    order_type: IOC
    side: BUY
    price: 61719.0
    quantity: 0.005609457341096823
    client_id: 4886581369384305006
Order transaction ID: 38DxpqDUXLetSwD1iJ3PsUBJ42fzYxpYeMk6uWucuLYQfAvPn5VcGrcwFxc5Rb2hgsxhBKLew7idAx3xGhqhaHtK
Need to settle open orders: « OpenOrders:
    Flags: « SerumAccountFlags: initialized | open_orders »
    Program ID: 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin
    Address: 2DCKHwbchxUDr2x2A7Z8YxKJojvv7gipTKwjyiZBbyvB
    Market: C1EuT9VokAKLiW7i2ASnZUvxDoKuKkCpDDeNxAptuNe4
    Owner: 48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB
    Base Token: 0.00560000 of 0.00560000
    Quote Token: 15.80494500 of 15.80494500
    Referrer Rebate Accrued: 144803
    Orders:
        None
    Client IDs:
        None
»
Base account: GzbKPy1TaM4gHNEBcVDKskEouePDopC5YRRLoFpPqkhm
Quote account: 2HchGy6FnjC6DuZb9oTZ9ByUMtUScJkhdDzGUkVNtc8T
Settlement transaction ID: 26nUTaeoKRPK7fQ4jCS216VVbVprqJGWbMn1NRC3vP3FXgnDFXrq1PthJgVWAuKAmmyixV77SrGwr2amox8ucrL3
Waiting on settlement transaction IDs: ['26nUTaeoKRPK7fQ4jCS216VVbVprqJGWbMn1NRC3vP3FXgnDFXrq1PthJgVWAuKAmmyixV77SrGwr2amox8ucrL3']
Waiting on specific settlement transaction ID: 26nUTaeoKRPK7fQ4jCS216VVbVprqJGWbMn1NRC3vP3FXgnDFXrq1PthJgVWAuKAmmyixV77SrGwr2amox8ucrL3
All settlement transaction IDs confirmed.
Order execution complete
BUY order market: 7dLVkUfBVfCGkFhSXDCq1ukM9usathSgS716t643iFGF <pyserum.market.market.Market object at 0x7f237d0b1ee0>
Price 3846.30750000000010 - adjusted by 0.05 from 3663.15000000000009094947017729282379150390625
Source token account: « AccountInfo [2HchGy6FnjC6DuZb9oTZ9ByUMtUScJkhdDzGUkVNtc8T]:
    Owner: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
    Executable: False
    Lamports: 2039280
    Rent Epoch: 179
»
Placing order
    paying_token_address: 2HchGy6FnjC6DuZb9oTZ9ByUMtUScJkhdDzGUkVNtc8T
    account: <solana.account.Account object at 0x7f237d147790>
    order_type: IOC
    side: BUY
    price: 3846.3075
    quantity: 0.09001342018264541
    client_id: 3766227519595772173
Order transaction ID: 63HUK1wNizrUJAYaMPxaQirni6AQp6BFgeqL8Uuw9cZhGJseqszLZkWFmMGPFWULKoHFuJSWMmX7kGQqNpxovvu8
Need to settle open orders: « OpenOrders:
    Flags: « SerumAccountFlags: initialized | open_orders »
    Program ID: 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin
    Address: E4jX61Z8w7uXpCiqU3amBKPdtf8qzpdrGvGFifNsxBAg
    Market: 7dLVkUfBVfCGkFhSXDCq1ukM9usathSgS716t643iFGF
    Owner: 48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB
    Base Token: 0.09000000 of 0.09000000
    Quote Token: 15.19678100 of 15.19678100
    Referrer Rebate Accrued: 145307
    Orders:
        None
    Client IDs:
        None
»
Base account: EeehKVmdzDatRzMgx8RGDAdnQ6XD1wTfWXHhD4aezrRM
Quote account: 2HchGy6FnjC6DuZb9oTZ9ByUMtUScJkhdDzGUkVNtc8T
Settlement transaction ID: 4Sb7qV8XL7vL3PsbLUuqtFHxcYbM3swu62T5ZMMsHewdWaaddDwaP1pK9jmANV5RBx9zh3vxuyGWfmh2xmwkFbAM
Waiting on settlement transaction IDs: ['4Sb7qV8XL7vL3PsbLUuqtFHxcYbM3swu62T5ZMMsHewdWaaddDwaP1pK9jmANV5RBx9zh3vxuyGWfmh2xmwkFbAM']
Waiting on specific settlement transaction ID: 4Sb7qV8XL7vL3PsbLUuqtFHxcYbM3swu62T5ZMMsHewdWaaddDwaP1pK9jmANV5RBx9zh3vxuyGWfmh2xmwkFbAM
All settlement transaction IDs confirmed.
Order execution complete
```

If you have problems at this stage, for example with Solana transactions timing out because of network problems, there are useful commands to manually fix things: `group-buy-token`, `group-sell-token` and (particularly useful for problems where Serum completes the order but the token doesn't make it to your wallet) `group-settle`.

Now if we check the balances we can see we have roughly a third in each of the three group tokens:
```
# mango-explorer group-balances
2021-05-08 14:31:43,910 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation

Balances:
    SOL balance:         0.94913592
    BTC balance:         0.00560000
    ETH balance:         0.09000000
   USDT balance:       339.20742600
```

We now have about 339 USDT, 0.0056 BTC, and 0.09 ETH. That's roughly a third each at today's prices.


# 10. ✅ Validate Account (Again)

Now would be a good time to run the `Account Scout` tool again, to make sure things are as we expect.
```
# mango-explorer account-scout
2021-05-08 14:34:10,009 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation

« ScoutReport [48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB]:
    Summary:
        No problems found

    Errors:
        None

    Warnings:
        None

    Details:
        Token account with mint '9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E' has balance: 0.0056 BTC
        Token account with mint '2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk' has balance: 0.09 ETH
        Token account with mint 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB' has balance: 339.207426 USDT
        Serum open orders account for market 'BTC/USDT': « OpenOrders:
            Flags: « SerumAccountFlags: initialized | open_orders »
            Program ID: 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin
            Address: 2DCKHwbchxUDr2x2A7Z8YxKJojvv7gipTKwjyiZBbyvB
            Market: C1EuT9VokAKLiW7i2ASnZUvxDoKuKkCpDDeNxAptuNe4
            Owner: 48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB
            Base Token: 0.00000000 of 0.00000000
            Quote Token: 0.00000000 of 0.00000000
            Referrer Rebate Accrued: 0
            Orders:
                None
            Client IDs:
                None
        »
        Serum open orders account for market 'ETH/USDT': « OpenOrders:
            Flags: « SerumAccountFlags: initialized | open_orders »
            Program ID: 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin
            Address: E4jX61Z8w7uXpCiqU3amBKPdtf8qzpdrGvGFifNsxBAg
            Market: 7dLVkUfBVfCGkFhSXDCq1ukM9usathSgS716t643iFGF
            Owner: 48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB
            Base Token: 0.00000000 of 0.00000000
            Quote Token: 0.00000000 of 0.00000000
            Referrer Rebate Accrued: 0
            Orders:
                None
            Client IDs:
                None
        »
        Account '48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB' has no Mango Markets margin accounts.
»
```

You can see that the process of balancing the tokens has created the necessary token accounts, as well as creating the `OpenOrders` accounts Serum uses for trading.

All looks good now!


# 11. 🎬 Start The (Pretend) Liquidator

OK, now we're ready to try a test run of the liquidator.

This is a long-running process, so we'll need to use Control-C to cancel it when we're done.

Here goes:
```
# mango-explorer liquidator --target "BTC:33%" --target "ETH:33%" --dry-run
2021-05-08 14:36:34,200 WARNING  root
⚠ WARNING ⚠

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    🥭 Mango Markets: https://mango.markets
    📄 Documentation: https://docs.mango.markets/
    💬 Discord: https://discord.gg/67jySBhxrg                                                                       🐦 Twitter: https://twitter.com/mangomarkets
    🚧 Github: https://github.com/blockworks-foundation                                                             📧 Email: mailto:hello@blockworks.foundation

2021-05-08 14:36:34,206 INFO     root         Context: « Context:                                                                     Cluster: mainnet-beta
    Cluster URL: https://mango.rpcpool.com/
    Program ID: JD3bq9hGdy38PuWQ4h2YJpELmHVGPPfFSuFkpzAd9zfu
    DEX Program ID: 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin
    Group Name: BTC_ETH_USDT
    Group ID: 7pVYhpKUHw88neQHxgExSH6cerMZ1Axx1ALQP9sxtvQV
»
2021-05-08 14:36:34,209 INFO     root         Wallet address: 48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB
2021-05-08 14:36:34,251 INFO     root         Checking wallet accounts.
2021-05-08 14:36:37,032 INFO     root         Wallet account report: « ScoutReport [48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB]:
    Summary:
        No problems found

    Errors:
        None

    Warnings:
        None

    Details:
        Token account with mint '9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E' has balance: 0.0056 BTC
        Token account with mint '2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk' has balance: 0.09 ETH
        Token account with mint 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB' has balance: 339.207426 USDT
        Serum open orders account for market 'BTC/USDT': « OpenOrders:
            Flags: « SerumAccountFlags: initialized | open_orders »
            Program ID: 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin
            Address: 2DCKHwbchxUDr2x2A7Z8YxKJojvv7gipTKwjyiZBbyvB
            Market: C1EuT9VokAKLiW7i2ASnZUvxDoKuKkCpDDeNxAptuNe4
            Owner: 48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB
            Base Token: 0.00000000 of 0.00000000
            Quote Token: 0.00000000 of 0.00000000
            Referrer Rebate Accrued: 0
            Orders:
                None
            Client IDs:
                None
        »
        Serum open orders account for market 'ETH/USDT': « OpenOrders:
            Flags: « SerumAccountFlags: initialized | open_orders »
            Program ID: 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin
            Address: E4jX61Z8w7uXpCiqU3amBKPdtf8qzpdrGvGFifNsxBAg
            Market: 7dLVkUfBVfCGkFhSXDCq1ukM9usathSgS716t643iFGF
            Owner: 48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB
            Base Token: 0.00000000 of 0.00000000
            Quote Token: 0.00000000 of 0.00000000
            Referrer Rebate Accrued: 0
            Orders:
                None
            Client IDs:
                None
        »
        Account '48z8UzFTYYbmFGgryA3muJ4tjdPsDUnB84YvfCXtv4dB' has no Mango Markets margin accounts.
»
2021-05-08 14:36:37,042 INFO     root         Wallet accounts OK.
2021-05-08 14:36:37,042 INFO     SimpleLiquidator Fetching all margin accounts...
2021-05-08 14:36:53,162 INFO     SimpleLiquidator Fetched 15065 margin accounts to process.
2021-05-08 14:36:53,712 INFO     SimpleLiquidator Of those 15065, 3644 have a nonzero collateral ratio.
2021-05-08 14:36:53,718 INFO     SimpleLiquidator Of those 3644, 69 are liquidatable.
2021-05-08 14:36:53,720 INFO     SimpleLiquidator Of those 69 liquidatable margin accounts, 3 are 'above water' margin accounts with assets greater than their liabilities.
2021-05-08 14:36:53,721 INFO     SimpleLiquidator Of those 3 above water margin accounts, 0 are worthwhile margin accounts with more than 0.01 net assets.
2021-05-08 14:36:53,721 INFO     SimpleLiquidator No accounts to liquidate.
2021-05-08 14:36:54,096 INFO     root         Check of all margin accounts complete. Time taken: 17.05 seconds, sleeping for 43 seconds...
2021-05-08 14:37:37,142 INFO     SimpleLiquidator Fetching all margin accounts...
2021-05-08 14:37:53,634 INFO     SimpleLiquidator Fetched 15065 margin accounts to process.
2021-05-08 14:37:54,112 INFO     SimpleLiquidator Of those 15065, 3644 have a nonzero collateral ratio.
2021-05-08 14:37:54,119 INFO     SimpleLiquidator Of those 3644, 69 are liquidatable.
2021-05-08 14:37:54,120 INFO     SimpleLiquidator Of those 69 liquidatable margin accounts, 3 are 'above water' margin accounts with assets greater than their liabilities.
2021-05-08 14:37:54,121 INFO     SimpleLiquidator Of those 3 above water margin accounts, 0 are worthwhile margin accounts with more than 0.01 net assets.
2021-05-08 14:37:54,121 INFO     SimpleLiquidator No accounts to liquidate.
2021-05-08 14:37:54,513 INFO     root         Check of all margin accounts complete. Time taken: 17.37 seconds, sleeping for 43 seconds...
^C2021-05-08 14:38:36,341 INFO     root         Stopping...
2021-05-08 14:38:36,341 INFO     root         Liquidator completed.

```

Well, that all seemed fine.

Some important things to note from the simulated run:
* It does a bunch of checks on startup to make sure it is in a state that can run.
* It prints out some summary information about the wallet account and child accounts.
* It loops once per minute, assessing which margin accounts are liquidatable (none, in the above run)
* It sleeps for as long as it can between runs
* You can't see it in the above (because no liquidations occurred) but it will automatically balance the wallet after every liquidation.


# 12. ⚡ Really Start The Liquidator

Remember that section on ☠️ Risks above? Well, if you still want to do it - **and I’m not recommending you do** - you can have `liquidator` submit live orders by removing the `--dry-run` parameter.

Output should be broadly the same as the output for a 'dry run', but if it sees any worthwhile liquidatable accounts it should try to perform a partial liquidation.

Now, it's over to you. Happy liquidating!